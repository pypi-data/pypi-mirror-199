import asyncio
import gc
import os

import aioredis
import pytest
import siderpy
import uvloop


REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)


if os.environ.get("UVLOOP"):
    uvloop.install()
    new_event_loop = uvloop.new_event_loop
else:
    new_event_loop = asyncio.new_event_loop


@pytest.fixture(scope="function")
def event_loop(request):
    loop = new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()


def siderpy_setup(loop):
    return siderpy.Redis(f"redis://{REDIS_HOST}:{REDIS_PORT}")


def siderpy_teardown(loop, redis):
    loop.run_until_complete(redis.close())


def siderpy_pool_setup(loop):
    return siderpy.RedisPool(f"redis://{REDIS_HOST}:{REDIS_PORT}")


def siderpy_pool_teardown(loop, redis):
    loop.run_until_complete(redis.close())


def aioredis_setup(loop):
    return aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")


def aioredis_teardown(loop, redis):
    loop.run_until_complete(redis.close())


@pytest.fixture(
    params=[
        pytest.param((aioredis_setup, aioredis_teardown), id="aioredis"),
        pytest.param((siderpy_setup, siderpy_teardown), id="siderpy"),
        pytest.param((siderpy_pool_setup, siderpy_pool_teardown), id="siderpy_pool"),
    ],
    scope="function",
)
def redis(event_loop, request):
    setup, teardown = request.param
    cli = setup(event_loop)
    try:
        event_loop.run_until_complete(cli.flushall())
        yield cli
    finally:
        teardown(event_loop, cli)


@pytest.fixture
def gc_collect():
    gc.collect()
    yield


def execute(loop, count, coro_func, *args, **kwds):
    for _ in range(count):
        loop.run_until_complete(coro_func(*args, **kwds))


class TestBenchmark:
    @pytest.mark.benchmark(
        group="ping",
        disable_gc=True,
        min_rounds=50,
    )
    def test_ping(self, event_loop, gc_collect, benchmark, redis):
        async def call():
            for _ in range(30):
                await redis.ping()

        benchmark(execute, event_loop, 5, call)

    @pytest.mark.benchmark(
        group="set",
        disable_gc=True,
        min_rounds=50,
    )
    def test_set(self, event_loop, gc_collect, benchmark, redis):
        async def call():
            for _ in range(30):
                await redis.set("key", "value")

        benchmark(execute, event_loop, 5, call)

    @pytest.mark.benchmark(
        group="get",
        disable_gc=True,
        min_rounds=50,
    )
    def test_get(self, event_loop, gc_collect, benchmark, redis):
        async def call():
            for _ in range(30):
                await redis.get("key")

        benchmark(execute, event_loop, 5, call)

    @pytest.mark.benchmark(
        group="mget",
        disable_gc=True,
        min_rounds=50,
    )
    def test_mget(self, event_loop, gc_collect, benchmark, redis):
        async def call():
            count = 250
            keys = [f"key{i}" for i in range(count)]
            for _ in range(5):
                for i in range(count):
                    await redis.set(f"key{i}", f"value{i}")
                await redis.mget(*keys)

        benchmark(execute, event_loop, 1, call)

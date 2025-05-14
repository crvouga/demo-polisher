from kv.factory import KvFactory


class Fixture:
    def __init__(self):
        self.kv = KvFactory.create("dict")

        self.test_key = "test_key"
        self.test_value = "test_value"


async def test_put_get(self):
    """Test basic put and get operations"""
    f = Fixture()
    # Test putting a value
    success = await f.kv.put(f.test_key, f.test_value)
    assert success is True

    # Test getting the value back
    value = await f.kv.get(f.test_key)
    assert value == f.test_value


async def test_get_nonexistent(self):
    """Test getting a nonexistent key returns None"""
    f = Fixture()
    value = await f.kv.get("nonexistent_key")
    assert value is None


async def test_zap(self):
    """Test zap operation"""
    f = Fixture()
    # First put a value
    await f.kv.put(f.test_key, f.test_value)

    # Test zapping it
    success = await f.kv.zap(f.test_key)
    assert success is True

    # Verify it's gone
    value = await f.kv.get(f.test_key)
    assert value is None


async def test_zap_nonexistent(self):
    """Test zapping a nonexistent key returns False"""
    f = Fixture()
    success = await f.kv.zap("nonexistent_key")
    assert success is False


async def test_put_update(self):
    """Test updating an existing key"""
    f = Fixture()
    # Put initial value
    await f.kv.put(f.test_key, f.test_value)

    # Update with new value
    new_value = "new_value"
    success = await f.kv.put(f.test_key, new_value)
    assert success is True

    # Verify update
    value = await f.kv.get(f.test_key)
    assert value == new_value

from ..services.threshold.thresholdbase import ThresholdBase as t
from ..models.const import CURRENTS_THREEPHASE_1_32
import pytest

@pytest.mark.asyncio
async def test__start():
    ret = await t._start(50, False)
    assert ret == 83.49

@pytest.mark.asyncio
async def test__start_caution_non_caution_late():
    ret = await t._start(50, False)
    ret2 = await t._start(50, True)
    assert ret == ret2

@pytest.mark.asyncio
async def test__start_caution_non_caution_early():
    ret = await t._start(40, False)
    ret2 = await t._start(40, True)
    assert ret > ret2

@pytest.mark.asyncio
async def test__stop():
    ret = await t._stop(13, False)
    assert ret == 82.55

@pytest.mark.asyncio
async def test__stop_caution_non_caution_late():
    ret = await t._stop(50, False)
    ret2 = await t._stop(50, True)
    assert ret == ret2

@pytest.mark.asyncio
async def test__stop_caution_non_caution_early():
    ret = await t._stop(40, False)
    ret2 = await t._stop(40, True)
    assert ret > ret2

@pytest.mark.asyncio
async def test_allowed_current_base():
    ret = await t.allowed_current(
        now_min=0,
        moving_avg=1,
        charger_enabled=False,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0,
        peak=1
    )
    assert ret == t.BASECURRENT

@pytest.mark.asyncio
async def test_allowed_current_1():
    ret = await t.allowed_current(
        now_min=10,
        moving_avg=560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0.3,
        peak=10
    )
    assert ret == 16

@pytest.mark.asyncio
async def test_allowed_current_2():
    ret = await t.allowed_current(
        now_min=50,
        moving_avg=560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0.3,
        peak=10
    )
    assert ret == 32

@pytest.mark.asyncio
async def test__start_quarterly():
    ret = await t._start(50, False, True)
    assert ret == 60.62

@pytest.mark.asyncio
async def test__start_quarterly_caution():
    ret = await t._start(50, True, True)
    assert ret == 52.13

@pytest.mark.asyncio
async def test__stop_quarterly():
    ret = await t._start(22, False, True)
    assert ret == 65.29

@pytest.mark.asyncio
async def test__stop_quarterly_caution():
    ret = await t._start(22, True, True)
    assert ret == 58.06

@pytest.mark.asyncio
async def test_allowed_current_negative_movingavg():
    ret = await t.allowed_current(
        now_min=10,
        moving_avg=-560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=0.3,
        peak=10
    )
    assert ret == 16

@pytest.mark.asyncio
async def test_allowed_current_negative_totalenergy():
    ret = await t.allowed_current(
        now_min=10,
        moving_avg=560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=-0.3,
        peak=10
    )
    assert ret == 16

@pytest.mark.asyncio
async def test_allowed_current_negative_totalenergy_and_movingavg():
    ret = await t.allowed_current(
        now_min=10,
        moving_avg=-1560,
        charger_enabled=True,
        charger_done=False,
        currents_dict=CURRENTS_THREEPHASE_1_32,
        total_energy=-0.3,
        peak=10
    )
    assert ret == 20
"""
Integration Test: LIA Closed-Loop Protection for CAHAYA Sovereign AI
Test Case B — Vector Store Corruption & Recovery
"""

from core.event_bus import EventBus, NormalizedEvent
from shield.engine import ShieldEngine, PolicyDecision
from reflex.engine import ReflexEngine
from heal.pipeline import RecoveryPipeline
from memory.store import ImmuneMemoryStore

class MockCahayaVectorStore:
    def __init__(self):
        self.state = "HEALTHY"
        self.data = {"doc_1": "valid_embedding_vector"}
        self.writes_enabled = True

    def corrupt(self):
        self.state = "CORRUPTED"
        self.data["doc_1"] = "CORRUPTED_BYTES"

    def halt_writes(self):
        self.writes_enabled = False

    def restore_from_checkpoint(self) -> dict:
        return {"doc_1": "valid_embedding_vector"}

    def validate_integrity(self, candidate_data: dict) -> bool:
        return candidate_data.get("doc_1") == "valid_embedding_vector"

def test_closed_loop_cahaya_vector_recovery():
    # Setup LIA Core Organs
    bus = EventBus()
    shield = ShieldEngine(bus)
    reflex = ReflexEngine(bus)
    heal = RecoveryPipeline(bus)
    memory = ImmuneMemoryStore(bus)

    cahaya_vector_store = MockCahayaVectorStore()

    # Register Reflex Action
    def on_state_corruption(event: NormalizedEvent):
        cahaya_vector_store.halt_writes()

    reflex.register_handler("FREEZE_PROCESS", on_state_corruption)

    # STEP 1: Introduce Failure / Attack
    cahaya_vector_store.corrupt()
    assert cahaya_vector_store.state == "CORRUPTED"

    # STEP 2: Vision Observes & Emits Anomaly Event
    bus.publish(NormalizedEvent(
        event_type="ANOMALY_DETECTED",
        source="vision_observer",
        component="cahaya_vector_store",
        severity="HIGH",
        metadata={"anomaly": "vector_index_checksum_mismatch"}
    ))

    # STEP 3: Reflex Contains Threat (Halts Writes)
    assert cahaya_vector_store.writes_enabled is False

    # STEP 4: Heal Executes Bounded Recovery Pipeline
    recovered_data = {}

    def diagnose():
        return {"last_good_checkpoint": "cp_1002"}

    def recover(diag):
        nonlocal recovered_data
        recovered_data = cahaya_vector_store.restore_from_checkpoint()
        return True

    def validate():
        return cahaya_vector_store.validate_integrity(recovered_data)

    def rollback():
        pass

    heal_success = heal.execute_recovery(
        component="cahaya_vector_store",
        diagnose_fn=diagnose,
        recovery_fn=recover,
        validate_fn=validate,
        rollback_fn=rollback
    )

    # STEP 5: Verification & Resumption
    assert heal_success is True
    cahaya_vector_store.state = "HEALTHY"
    cahaya_vector_store.data = recovered_data
    cahaya_vector_store.writes_enabled = True

    assert cahaya_vector_store.state == "HEALTHY"
    assert cahaya_vector_store.data["doc_1"] == "valid_embedding_vector"

    # STEP 6: Immune Memory Recorded
    records = memory.records
    assert len(records) > 0
    event_types = [r["event_type"] for r in records]
    assert "ANOMALY_DETECTED" in event_types
    assert "HEAL_VALIDATED" in event_types

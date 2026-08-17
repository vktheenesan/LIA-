"""
LIA Immune Memory — Cryptographically Signed Structured Incident Memory (Ed25519)
"""

import json
import hashlib
from typing import List, Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from core.event_bus import EventBus, NormalizedEvent

class ImmuneMemoryStore:
    """
    Structured, tamper-evident incident memory utilizing Ed25519 asymmetric signatures.
    """

    def __init__(self, event_bus: EventBus, private_key: Optional[ed25519.Ed25519PrivateKey] = None):
        self.event_bus = event_bus
        self.records: List[Dict[str, Any]] = []
        
        # Ed25519 Private Key Generation
        if private_key is None:
            self.private_key = ed25519.Ed25519PrivateKey.generate()
        else:
            self.private_key = private_key
            
        self.public_key = self.private_key.public_key()
        self.event_bus.subscribe_all(self._record_event)

    def _record_event(self, event: NormalizedEvent):
        # Record security-relevant events
        if event.severity in ("WARNING", "HIGH", "CRITICAL") or "POLICY" in event.event_type or "HEAL" in event.event_type:
            payload = self._get_payload_string(event)
            sha256_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            ed25519_sig = self.private_key.sign(payload.encode("utf-8")).hex()

            record = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "source": event.source,
                "component": event.component,
                "severity": event.severity,
                "metadata": event.metadata,
                "sha256_hash": sha256_hash,
                "ed25519_signature": ed25519_sig,
                "payload_str": payload
            }
            self.records.append(record)

    def _get_payload_string(self, event: NormalizedEvent) -> str:
        return f"{event.event_id}:{event.event_type}:{event.timestamp}:{event.component}:{event.severity}"

    def verify_record(self, record: Dict[str, Any]) -> bool:
        """
        Cryptographically verifies the record using the daemon's Ed25519 public key.
        """
        try:
            payload = record.get("payload_str", "")
            sig_bytes = bytes.fromhex(record.get("ed25519_signature", ""))
            self.public_key.verify(sig_bytes, payload.encode("utf-8"))
            
            # Also verify SHA256 integrity
            computed_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            if computed_hash != record.get("sha256_hash"):
                return False
                
            return True
        except Exception:
            return False

    def get_records(self) -> List[Dict[str, Any]]:
        return list(self.records)

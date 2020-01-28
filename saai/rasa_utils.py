import logging
import json
logger = logging.getLogger(__name__)

def dump_slots(tracker):
    logging.info('.. slots')
    logging.info(json.dumps(tracker.current_slot_values(), indent=2, ensure_ascii=False))


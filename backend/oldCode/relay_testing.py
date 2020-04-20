import time

import relay

def test_relays():
    for r in relay.RELAYS:
        relay.all_off()
        time.sleep(0.25)
        relay.set_relay(r, relay.RELAY_ON)
        time.sleep(1)
    relay.all_off()

if __name__ == '__main__':
    print('Initializing relays...')
    relay.init_relays()

    print('Testing relays...')
    test_relays()

    print('Done')

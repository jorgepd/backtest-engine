

def main_loop(bars, event_q, port, broker, strategies):
    # execution loop
    while True:
        # update bars, stop if no more data
        try:
            bars.update_bars()
        except StopIteration:
            break

        # handle events queue
        while True:
            # get next event
            try:
                event = event_q.popleft()
            except IndexError:
                break

            # route each event properly
            if event.type == 'MARKET':
                for s in strategies:
                    s.calc_signals()
                port.update_timeindex()

            elif event.type == 'SIGNAL':
                port.update_signal(event)

            elif event.type == 'ORDER':
                broker.execute_order(event)

            elif event.type == 'FILL':
                port.update_fill(event)

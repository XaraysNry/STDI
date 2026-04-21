from vector_clock import VectorClock

vc0 = VectorClock(3, 0)
vc1 = VectorClock(3, 1)

vc0.increment()
msg = vc0.send_message()

vc1.receive_message(msg)

print(vc0)
print(vc1)

print("Happens before:", vc0.happens_before(vc1))
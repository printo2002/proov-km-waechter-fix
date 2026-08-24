# What I checked, and what the agent got wrong

## What the agent got wrong

As mentioned, first I prompted the agent to give a summary of the entire codebase. The
agent gave a detailed summary and listed the errors in the code. But it could not detect
the old Python style on its own, and the task for analyze.py was not done until I
explicitly asked for it.

Even though I mentioned all the specific details in one prompt, I had to re-mention some
of them before the agent made the corrections properly. For example the box-drawing
characters in analyze.py caused a crash on Windows and the agent took two attempts to
fully fix it.

## What I checked before I accepted its work

Bugs were identified by the agent as per my request. I verified the 80 percent rule
myself by reading the constants in km_wachter.py and confirming SERVICE_INTERVAL_KM is
still 15000 and WARN_AT_PERCENT is still 80. The agent also confirmed this in the chat
and verify.py showed PASS for that check.

## What the data actually said

The obvious guess was that older, higher-mileage cars break down more. The data does not
support that at all. Total odometer mileage and age have almost zero correlation with
breakdowns.

The real signal is how many kilometres the car has driven since its last service. Broke-down
cars drove an average of 11,678 km since their last service, compared to 7,261 km for cars
that survived. That is a 61 percent difference and it is the strongest predictor in the
dataset. Load factor also separates the two groups but less strongly.

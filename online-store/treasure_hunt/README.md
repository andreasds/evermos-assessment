# Treasure Hunt

* Treasure map layout defined at file [treasure-map.layout](treasure-map.layout)
* \# represents an obsacle
* . represents a clear path
* X represents the player's starting position
* A treasure is hidden within one of the clear path points

## Rule Navigation

The user must navigate in a specific order:

* Up / North `A` step(s), then
* Right / East `B` step(s), then
* Down / South `C` step(s)
* `A`, `B`, `C` > 0

## How to run

```bash
./scripts/run.sh
```

## How to Run manually

```bash
python -m treasure_hunt
```

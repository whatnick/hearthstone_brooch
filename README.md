# HearthStone Brooch

An electronics wearable in the shape of the 8-point hearthstone star

## Project Layout

```mermaid
graph TB
A[Root]-->D[docs - Documentation]
A-->HE[ecad - KiCAD electronics]
A-->HM[mcad - FreeCAD 3D objects]
A-->F[firmware - Arduino Firmware]
A-->S[software - Python SOftware]
```
## Electronics Design

## Mechanical Design
FreeCAD Assemblies with :
- Front of the brooch
- Rear lid + putting on pin

## Arduino Firmware Functions
- Creates progressive brightness shift of LED's to create breathing pattern
- Turns lighting effect on and off
- Any other hardware enhancement functions we dream of

## Python Software
- Generates pattern arrays for the blinking waveform.
- Parametrically generates Brooch with [Cadquery](https://github.com/CadQuery/cadquery)

**NOTE** : This is purely a hobby item. Replicate at your own risk.


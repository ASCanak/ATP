# ATP Slaapkamer Comfort-Regelsysteem
Bij dit project wordt er een Slaapkamer Comfort-Regelsysteem gesimuleerd. Het regelsysteem zal worden gesimuleerd in Python en de hardware zal worden gemocked in C++ de twee desbetreffende modules zullen aan elkaar worden gekoppeld doormiddel van DLCC.

## Gekozen sensoren en actuatoren
- Sensoren: 
  - BH1750 (Licht)
  - DHT11  (Temperatuur)
- Actuatoren:
  - Generieke Koelunit     (Aan/Uit/Status)
  - Generieke Rolluikmotor (Aan/Uit/Status)
 
## Vereisten
- Python 3.7.16 ( Wellicht werkt een andere python versie ook. )
- C++ Compiler ( g++ )
- Linux (Windows ondersteund geen .so files)

## Aanmaken van C(++)-Binding
```bash
g++ -shared -o clibrary.so -fPIC ./sources/B* ./sources/K* ./sources/R*
```
## Runnen van de simulator
```bash
python3 main.py
```
## Runnen van de tests
1. Unit Tests
```bash
python3 -m unittest unitTest.py
```
2. Integration Tests
```bash
python3 -m unittest integrationTest.py
```
3. System Test
```bash
python3 -m unittest systemTest.py
```

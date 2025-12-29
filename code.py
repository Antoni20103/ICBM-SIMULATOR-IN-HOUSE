import machine
import time
import math
import random
import array
import uctypes

# ========== KONFIGURACJA SPRZĘTOWA ==========
BUZZER_PIN = machine.Pin(19)
LED_GREEN = machine.Pin(17, machine.Pin.OUT)
LED_RED = machine.Pin(14, machine.Pin.OUT)

# Zaawansowana konfiguracja PWM
buzzer = machine.PWM(BUZZER_PIN)
buzzer.freq(1000)
buzzer.duty_u16(0)

# Stałe audio
SAMPLE_RATE = 40000  # Hz dla lepszej jakości dźwięku
PWM_RANGE = 65535
DUTY_MIN = 1000
DUTY_MAX = 30000

# ========== ZAAWANSOWANE FUNKCJE DŹWIĘKU ==========


class AdvancedAudio:
    def __init__(self):
        self.phase = 0.0
        self.noise_seed = 12345

    def brownian_noise(self, amount=0.3):
        """Generuje szum brunatny (Brownian noise)"""
        self.noise_seed = (self.noise_seed * 1103515245 + 12345) & 0x7fffffff
        return ((self.noise_seed / 0x7fffffff) - 0.5) * 2 * amount

    def frequency_sweep(self, start_hz, end_hz, duration_ms, curve=1.0):
        """Płynna zmiana częstotliwości z krzywą"""
        steps = int(duration_ms * SAMPLE_RATE / 1000)
        for i in range(steps):
            t = i / steps
            # Nieliniowa krzywa (exponential)
            if curve != 1.0:
                t = math.pow(t, curve)
            freq = start_hz + (end_hz - start_hz) * t
            self.set_frequency_advanced(freq, 0.1)
            time.sleep_ms(1)

    def set_frequency_advanced(self, freq_hz, noise_amount=0.05):
        """Ustawia częstotliwość z dodanym szumem i wibracjami"""
        if freq_hz <= 0:
            buzzer.duty_u16(0)
            return

        # Dodaj subtelny szum do częstotliwości
        noise = self.brownian_noise(noise_amount)
        actual_freq = freq_hz * (1.0 + noise)

        # Ogranicz zakres
        actual_freq = max(20, min(5000, actual_freq))

        # Ustaw częstotliwość z losową modulacją PWM dla "chropowatości"
        buzzer.freq(int(actual_freq))

        # Dynamiczna zmiana wypełnienia dla efektów
        duty = DUTY_MIN + \
            int((math.sin(time.ticks_ms() / 50) * 0.5 + 0.5) * (DUTY_MAX - DUTY_MIN))
        buzzer.duty_u16(duty)

    def complex_waveform(self, base_freq, harmonics, duration_ms):
        """Generuje złożony dźwięk z harmonicznymi"""
        steps = int(duration_ms * 100)
        for i in range(steps):
            # Suma sinusoid dla harmonicznych
            freq_variation = 0
            for h, amp in enumerate(harmonics, 1):
                freq_variation += amp * \
                    math.sin(2 * math.pi * h * base_freq * i / 1000)

            actual_freq = base_freq * (1.0 + freq_variation * 0.1)
            self.set_frequency_advanced(actual_freq, 0.02)
            time.sleep_ms(10)

# ========== REALISTYCZNE EFEKTY DŹWIĘKOWE ==========


audio = AdvancedAudio()


def realistic_countdown():
    """Realistyczne odliczanie z systemem alarmowym"""
    print("🚨 REALISTYCZNE ODLICZANIE STARTU")

    LED_GREEN.value(1)

    # Niskie buczenie systemów
    for i in range(3):
        audio.set_frequency_advanced(180, 0.01)
        LED_RED.value(1)
        time.sleep(0.5)
        audio.set_frequency_advanced(0, 0)
        LED_RED.value(0)
        time.sleep(0.5)

    # Głos syntezatora odliczania (seria krótkich sygnałów)
    countdown_freqs = [(800, 0.3), (900, 0.2), (1000, 0.1), (1200, 0.4)]
    for count, (freq, duration) in enumerate(countdown_freqs, 7):
        print(f"T-{count}")

        # Sygnał odliczania
        audio.set_frequency_advanced(freq, 0.01)
        LED_RED.value(1)
        LED_GREEN.value(0)
        time.sleep(duration)

        # Przerwa z niskim buczeniem
        audio.set_frequency_advanced(150, 0.02)
        LED_RED.value(0)
        LED_GREEN.value(1)
        time.sleep(1 - duration)

    # Ostatnie, intensywne odliczanie
    for freq in [1200, 0, 1400, 0, 1600, 0, 2000]:
        audio.set_frequency_advanced(freq, 0.05)
        LED_RED.value(1)
        LED_GREEN.value(1 if freq == 0 else 0)
        time.sleep(0.15)


def rocket_engine_start():
    """Ultra-realistyczny rozruch silnika rakietowego"""
    print("🔥 ROZRUCH SILNIKA RAKIETOWEGO")

    # 1. Zapłon starterów (krótki, wysoki pisk)
    audio.set_frequency_advanced(3000, 0.1)
    LED_RED.value(1)
    time.sleep(0.1)

    # 2. Początkowe buczenie palników
    audio.frequency_sweep(2000, 800, 300, 0.7)

    # 3. Głębokie, narastające buczenie głównego silnika
    for i in range(100):
        # Nieliniowe narastanie
        progress = i / 100
        freq = 80 + (220 * math.pow(progress, 1.5))

        # Dodaj wibracje silnika
        vibration = math.sin(progress * 50) * 15 * (1 + progress)
        actual_freq = freq + vibration

        # Modulacja PWM dla efektu "chropawego" dźwięku
        duty_mod = math.sin(progress * 30) * 5000 + 15000
        buzzer.duty_u16(int(duty_mod))

        audio.set_frequency_advanced(actual_freq, 0.08 + progress * 0.1)

        # Migotanie świateł symulujące wibracje
        LED_RED.value(1 if (i % 3) == 0 else 0)
        LED_GREEN.value(1 if (i % 5) == 0 else 0)

        time.sleep(0.02)

    print("✅ SILNIK NA PEŁNEJ MOCY")


def launch_phase():
    """Realistyczny start i początkowy lot"""
    print("🚀 FAZA STARTU")

    # Intensywny dźwięk startu z efektem Dopplera
    base_freq = 300

    for t in range(200):  # 2 sekundy lotu
        # Główna częstotliwość spada (efekt Dopplera)
        doppler_effect = 1.0 / (1.0 + t * 0.015)
        main_freq = base_freq * doppler_effect

        # Dodaj harmoniczne dla pełni dźwięku
        harmonics = math.sin(t * 0.5) * 40 + math.sin(t * 1.7) * 20

        # Szum aerodynamiczny rośnie z prędkością
        air_noise = min(0.3, t * 0.002)

        # Łączna częstotliwość
        freq = main_freq + harmonics

        # Dynamiczna modulacja PWM
        duty = 12000 + int(math.sin(t * 0.3) * 8000 + math.sin(t * 1.2) * 4000)
        buzzer.duty_u16(duty)

        audio.set_frequency_advanced(freq, air_noise)

        # Światła - intensywne migotanie podczas startu
        if t < 50:
            LED_RED.value(1)
            LED_GREEN.value(0)
        else:
            LED_RED.value(1 if (t % 4) < 2 else 0)
            LED_GREEN.value(1 if (t % 6) < 3 else 0)

        time.sleep(0.01)

    print("✅ RAKIETA W LOCIE")


def boost_phase():
    """Faza przyspieszenia silników pomocniczych"""
    print("💨 FAZA PRZYSPIESZENIA")

    # Zmienna częstotliwość z pulsacjami
    for phase in range(3):  # Trzy pulsy przyspieszenia
        print(f"Puls przyspieszenia {phase + 1}/3")

        for i in range(60):
            # Pulsacyjny charakter pracy silników
            pulse = math.sin(i * 0.3) * 0.5 + 0.5
            base_freq = 180 + pulse * 100

            # Dodaj efekt "palenia się" paliwa
            combustion_noise = audio.brownian_noise(0.15)

            freq = base_freq * (1.0 + combustion_noise)

            # Gwałtowne zmiany wypełnienia PWM
            duty = 10000 + int((pulse + combustion_noise) * 15000)
            buzzer.duty_u16(duty)

            audio.set_frequency_advanced(freq, 0.12)

            # Intensywne miganie świateł
            LED_RED.value(1 if (i % 2) == 0 else 0)
            LED_GREEN.value(1 if (phase % 2) == 0 else 0)

            time.sleep(0.015)

        # Krótka przerwa między pulsami
        audio.set_frequency_advanced(100, 0.05)
        time.sleep(0.1)

    print("✅ PRZYSPIESZENIE ZAKOŃCZONE")


def midcourse_correction():
    """Korekta trajektorii w środkowej fazie lotu"""
    print("🎯 KOREKTA TRAJEKTORII")

    # Ciche buczenie systemów naprowadzania
    audio.set_frequency_advanced(120, 0.01)
    LED_GREEN.value(1)
    time.sleep(0.5)

    # Seria krótkich impulsów silników korekcyjnych
    for correction in range(5):
        # Impuls korekcyjny
        audio.frequency_sweep(400, 800, 50, 2.0)
        LED_RED.value(1)
        time.sleep(0.02)

        # Powrót do buczenia
        audio.set_frequency_advanced(120, 0.01)
        LED_RED.value(0)
        time.sleep(0.15 + random.random() * 0.1)

    print("✅ TRAJEKTORIA SKORYGOWANA")


def reentry_effects():
    """Ekstremalnie realistyczne wejście w atmosferę"""
    print("🌋 WEJŚCIE W ATMOSFERĘ")

    # Nagły wzrost szumu aerodynamicznego
    audio.set_frequency_advanced(80, 0.5)
    LED_RED.value(1)
    time.sleep(0.3)

    # Symulacja tarcia atmosferycznego
    for intensity in range(100):
        # Częstotliwość rośnie z temperaturą
        heat_effect = intensity * 4

        # Losowe "trzaski" i "wybuchy" powietrza
        crackle_freq = 0
        if random.random() > 0.7:
            crackle_freq = random.randint(1000, 3000)
            audio.set_frequency_advanced(crackle_freq, 0.3)
            time.sleep(0.02)

        # Główny dźwięk tarcia
        main_freq = 250 + heat_effect + math.sin(intensity * 0.5) * 50

        # Ekstremalna modulacja PWM dla efektu "chaosu"
        duty = 5000 + int((math.sin(intensity * 0.7) +
                          math.sin(intensity * 1.9)) * 10000)
        buzzer.duty_u16(duty)

        audio.set_frequency_advanced(main_freq, 0.4)

        # Szalone miganie świateł - systemy w stresie
        LED_RED.value(1 if (intensity % 3) == 0 else 0)
        LED_GREEN.value(1 if random.random() > 0.8 else 0)

        time.sleep(0.02)

    print("⚠️  KRYTYCZNE OGRZEWANIE")


def terminal_guidance():
    """Końcowe naprowadzanie na cel"""
    print("🎯 TERMINALNE NAPROWADZANIE")

    # Wysokie, stabilne buczenie systemu naprowadzania
    audio.set_frequency_advanced(600, 0.05)
    LED_GREEN.value(1)
    LED_RED.value(1)
    time.sleep(0.4)

    # Seria szybkich, precyzyjnych korekt
    for adjust in range(8):
        # Krótki, wysoki impuls korekcyjny
        audio.set_frequency_advanced(1200, 0.01)
        time.sleep(0.03)

        # Powrót do bazy
        audio.set_frequency_advanced(600, 0.05)
        time.sleep(0.07)

        # Mignięcie zielonym potwierdzeniem
        LED_GREEN.toggle()

    print("✅ CEL NAMIERZONY")


def nuclear_detonation_sequence():
    """Ultra-realistyczna sekwencja detonacji nuklearnej"""
    print("💣 SEKWENCJA DETONACJI")

    # 1. Ostateczne odliczanie detonacji
    for count in ["TRZY", "DWA", "JEDEN"]:
        print(count)

        # Rosnące buczenie zapalników
        audio.frequency_sweep(200, 500, 300, 1.5)
        LED_RED.value(1)
        time.sleep(0.1)

    # 2. Impuls inicjujący (bardzo krótki, bardzo wysoki)
    audio.set_frequency_advanced(4000, 0.1)
    buzzer.duty_u16(25000)
    LED_RED.value(1)
    LED_GREEN.value(1)
    time.sleep(0.05)

    # 3. Nagła cisza przed falą uderzeniową
    audio.set_frequency_advanced(0, 0)
    time.sleep(0.15)

    # 4. Fala uderzeniowa (ultra-realistyczna)
    print("💥 FALA UDERZENIOWA")

    # Niskie, narastające buczenie fali
    for i in range(80):
        # Nieliniowe narastanie
        t = i / 80
        freq = 30 + 200 * math.pow(t, 0.7)

        # Efekt "przytłaczania" - bardzo niskie tony
        sub_bass = math.sin(t * 10) * 15 * t

        # Modulacja PWM dla efektu "presji"
        duty = 8000 + int(t * 20000)
        buzzer.duty_u16(duty)

        audio.set_frequency_advanced(freq + sub_bass, 0.3 * t)

        # Światła - intensywne białe światło wybuchu
        if i < 40:
            LED_RED.value(1)
            LED_GREEN.value(1)
        else:
            # Migotanie podczas rozprzestrzeniania się fali
            LED_RED.value(1 if (i % 2) == 0 else 0)
            LED_GREEN.value(1 if (i % 3) == 0 else 0)

        time.sleep(0.015)

    # 5. Echo i rezonans
    print("🌪️  REZONANS I ECHA")

    for echo in range(10):
        # Zanikające echa
        echo_strength = math.pow(0.7, echo)
        freq = 80 * echo_strength

        audio.set_frequency_advanced(freq, 0.1 * echo_strength)

        # Pulsujące światła echa
        LED_RED.value(1)
        time.sleep(0.08 * echo_strength)
        LED_RED.value(0)
        LED_GREEN.value(1)
        time.sleep(0.08 * echo_strength)
        LED_GREEN.value(0)

        time.sleep(0.15)

    # 6. Ostateczny zanik (radioaktywny szum tła)
    print("☢️  PROMIENIOWANIE TŁA")

    for i in range(100):
        # Losowy szum radioaktywny
        freq = 50 + random.random() * 100
        noise = random.random() * 0.4

        audio.set_frequency_advanced(freq, noise)

        # Losowe migotanie uszkodzonej elektroniki
        if random.random() > 0.7:
            LED_RED.value(1)
            time.sleep(0.02)
            LED_RED.value(0)
        if random.random() > 0.8:
            LED_GREEN.value(1)
            time.sleep(0.01)
            LED_GREEN.value(0)

        time.sleep(0.05)

    # 7. Cisza
    audio.set_frequency_advanced(0, 0)
    LED_RED.value(0)
    LED_GREEN.value(0)

    print("✅ SEKWENCJA ZAKOŃCZONA")


def post_detonation_effects():
    """Efekty po detonacji - rozprzestrzenianie się fali"""
    print("🔥 POŻARY I BURZA OGNISTA")

    # Ciche, niestabilne buczenie pożarów
    for i in range(150):
        # Losowe "trzaski" ognia
        if random.random() > 0.9:
            audio.set_frequency_advanced(random.randint(800, 2000), 0.3)
            LED_RED.value(1)
            time.sleep(0.1)
            audio.set_frequency_advanced(0, 0)
            LED_RED.value(0)

        # Niskie buczenie żaru
        base_freq = 60 + math.sin(i * 0.1) * 20
        audio.set_frequency_advanced(base_freq, 0.15)

        # Migotanie jak płomienie
        LED_RED.value(1 if (i % 5) < 2 else 0)
        LED_GREEN.value(1 if random.random() > 0.95 else 0)

        time.sleep(0.1)

# ========== GŁÓWNA SEKWENCJA ==========


def full_realistic_icbm_sequence():
    """Pełna, ultra-realistyczna sekwencja ICBM"""

    print("\n" + "="*60)
    print("ULTRA-REALISTYCZNY SYMULATOR ICBM v2.0")
    print("SYSTEM RP2040 | PWM ADVANCED AUDIO")
    print("="*60)

    try:
        # 0. Inicjalizacja systemu
        print("\n[1/9] 💾 INICJALIZACJA SYSTEMU...")
        for i in range(5):
            LED_GREEN.value(1)
            audio.set_frequency_advanced(100, 0.01)
            time.sleep(0.1)
            LED_GREEN.value(0)
            audio.set_frequency_advanced(0, 0)
            time.sleep(0.1)

        # 1. Odliczanie
        realistic_countdown()
        time.sleep(0.5)

        # 2. Start silnika
        rocket_engine_start()
        time.sleep(0.3)

        # 3. Faza startu
        launch_phase()
        time.sleep(0.5)

        # 4. Przyspieszenie
        boost_phase()
        time.sleep(0.3)

        # 5. Korekta trajektorii
        midcourse_correction()
        time.sleep(0.5)

        # 6. Wejście w atmosferę
        reentry_effects()
        time.sleep(0.2)

        # 7. Naprowadzanie końcowe
        terminal_guidance()
        time.sleep(0.3)

        # 8. Detonacja
        nuclear_detonation_sequence()
        time.sleep(1)

        # 9. Efekty pokażowe
        post_detonation_effects()

        # Zakończenie
        print("\n" + "="*60)
        print("SYMULACJA ZAKOŃCZONA")
        print("="*60)

        # Trzykrotny sygnał końcowy
        for _ in range(3):
            audio.set_frequency_advanced(200, 0.01)
            LED_RED.value(1)
            time.sleep(0.1)
            audio.set_frequency_advanced(0, 0)
            LED_RED.value(0)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n⚠️  SEKWENCJA PRZERWANA")
    finally:
        # Gwarantowane wyczyszczenie
        audio.set_frequency_advanced(0, 0)
        LED_GREEN.value(0)
        LED_RED.value(0)
        buzzer.deinit()

# ========== URUCHOMIENIE ==========


def test_individual_phase():
    """Testowanie pojedynczej fazy"""
    phases = {
        '1': realistic_countdown,
        '2': rocket_engine_start,
        '3': launch_phase,
        '4': boost_phase,
        '5': reentry_effects,
        '6': nuclear_detonation_sequence
    }

    print("\nWybierz fazę do testowania:")
    for key in phases:
        print(f"{key}. {phases[key].__name__}")

    # W praktyce użyj input() jeśli masz konsolę
    # Dla Pico, po prostu uruchom pełną sekwencję


if __name__ == "__main__":
    # Uruchom pełną, realistyczną sekwencję
    full_realistic_icbm_sequence()

    # Lub testuj pojedyncze fazy:
    # test_individual_phase()

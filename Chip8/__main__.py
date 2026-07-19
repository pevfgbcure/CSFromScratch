import os
import sys
from argparse import ArgumentParser
from timeit import default_timer as timer

import pygame

from Chip8.constants import (
    ALLOWED_KEYS,
    FRAME_TIME_EXPECTED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TIMER_DELAY,
)
from Chip8.vm import VM


def run(program_data: bytes, name: str):
    """Run the virtual machine with the given program data and name.

    Args:
        program_data (bytes): The program data to run.
        name (str): The name of the program file.
    """
    # Start Pygame, create the window, and load the sound.
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    pygame.display.set_caption(f"Chip8 - {os.path.basename(name)}")
    beep_sound = pygame.mixer.Sound(
        os.path.dirname(os.path.realpath(__file__)) + "/beep.wav"
    )
    currently_playing_sound = False
    vm = VM(program_data)  # load the virtual machine with the program data.
    timer_accumulator = 0.0  # used to limit the timer to 60 Hz.
    # Main virtual machine loop.
    while True:
        frame_start = timer()
        vm.step()
        if vm.needs_redraw:
            pygame.surfarray.blit_array(screen, vm.display_buffer)
            pygame.display.flip()

        # Handle keyboard events.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name in ALLOWED_KEYS:
                    vm.keys[ALLOWED_KEYS.index(key_name)] = True
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                if key_name in ALLOWED_KEYS:
                    vm.keys[ALLOWED_KEYS.index(key_name)] = False
            elif event.type == pygame.QUIT:
                sys.exit()

        # Sound.
        if vm.play_sound:
            if not currently_playing_sound:
                beep_sound.play(-1)
                currently_playing_sound = True
            else:
                currently_playing_sound = False
                beep_sound.stop()

        # Handle timing.
        frame_end = timer()
        frame_time = frame_end - frame_start  # time the frame took in seconds.
        timer_accumulator += frame_time
        # Every 1/60 of a second decrement the timers.
        if timer_accumulator > TIMER_DELAY:
            vm.decrement_timers()
            timer_accumulator = 0
        # Limit the speed of the entire machine to FRAME_TIME_EXPECTED "frames" per second.
        if frame_time < FRAME_TIME_EXPECTED:
            difference = FRAME_TIME_EXPECTED - frame_time
            pygame.time.delay(int(difference * 1000))
            timer_accumulator += difference


if __name__ == "__main__":
    # Parse the file argument.
    file_parser = ArgumentParser("Chip8")
    file_parser.add_argument("rom_file", help="A file containing a CHIP-8 game.")
    arguments = file_parser.parse_args()
    with open(arguments.rom_file, "rb") as fp:
        file_data = fp.read()
        run(file_data, arguments.rom_file)

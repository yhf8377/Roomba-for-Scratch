# Roomba for Scratch provides an easy-to-use extension to the Scratch
# project (https://scratch.mit.edu) for controlling the Roomba  robots.
# Copyright (C) 2018  Frank Ye

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time

from enum import Enum, IntEnum

class Mode(IntEnum):
    NoChange = -1
    Off = 0
    Passive = 1
    Safe = 2
    Full = 3

class BaudRate(IntEnum):
    Baud300    = 0
    Baud600    = 1
    Baud1200   = 2
    Baud2400   = 3
    Baud4800   = 4
    Baud9600   = 5
    Baud14400  = 6
    Baud19200  = 7
    Baud28800  = 8
    Baud38400  = 9
    Baud57600  = 10
    Baud115200 = 11

class Weekday(IntEnum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

class Command(Enum):
    """
    Defines available OI commands.

    Each command is defined as a list containing the following values:

    allowed_modes:
        A list of modes that this command is allowed to be used. If the
        current mode of the OI does not allow this command an exception
        will be thrown.

    new_mode:
        The new mode the OI will switch into after executing the
        command.

    opcode_byte:
        The command code byte.

    data_bytes (optional):
        Zero or more bytes used for providing arguments to the command.
    """

    # Start to Passive mode
    Start =     [[Mode.Off, Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [128]]
    # Change Baud rate
    Baud =      [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [129, 0]]
    # Switch to Safe mode (same as Safe)
    Control =   [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Safe,
                 [130]]
    # Switch to Safe mode
    Safe =      [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Safe,
                 [131]]
    # Switch to Full mode
    Full =      [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Full,
                 [132]]
    # Power down the Roomba
    Power =     [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [133]]
    # Start spot cleaning procedure
    Spot =      [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [134]]
    # Start default cleaning procedure
    Clean =     [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [135]]
    # Start maximum cleaning procedure
    Max =       [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [136]]
    # Drive the Roomba
    Drive =     [[Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [137, 0, 0, 0, 0]]
    # Set vacuum/brush motor direction and on/off state
    Motors =    [[Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [138, 0]]
    # Store songs into Roomba
    Song =      [[Mode.Passive, Mode.Safe, Mode.Full],
                Mode.NoChange,
                [140, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # Store songs into Roomba
    Play =      [[Mode.Safe, Mode.Full],
                Mode.NoChange,
                [141, 0]]
    # Start docking procedure
    Dock =      [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.Passive,
                 [143]]
    # Set vacuum/brush motor direction and speed using PWM
    PwmMotors = [[Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [144, 0, 0, 0]]
    # Drive the Roomba directly
    DirDrive =  [[Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [145, 0, 0, 0, 0]]
    # Drive the Roomba using PWM
    PwmDrive =  [[Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [146, 0, 0, 0, 0]]
    # Change cleaning schedule
    Schedule =  [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [167, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # Set Roomba's clock date and time
    SetClock =  [[Mode.Passive, Mode.Safe, Mode.Full],
                 Mode.NoChange,
                 [168, 0, 0, 0]]

class RoombaOI:
    """
    Implements raw serial communication over Roomba Open Interface (OI).
    """

    def __init__(self, comm_device):
        self.current_mode = Mode.Off
        self.comm_device = comm_device
        self.send_command(Command.Start)
    
    def send_command(self, command, extra=None):
        if self.current_mode not in command.value[0]:
            raise ValueError('Command "%s" not allowed in "%s" mode'
                             % (command.name, self.current_mode))

        payload = [command.value[2][0]]
        if extra is not None:
            payload.extend(extra)
        try:
            payload = [max(0, min(x, 255)) for x in payload]
            self.comm_device.send(bytes(payload))
            time.sleep(0.05)
            if command.value[1] != Mode.NoChange:
                self.current_mode = command.value[1]
        except:
            pass
    
    def set_mode(self, new_mode):
        """
        Change the mode of the Roomba.

        Args:
            new_mode: a value from the Mode enum
        
        Raises:
            ValueError
        """

        if new_mode == Mode.Passive:
            self.send_command(Command.Start)
        elif new_mode == Mode.Safe:
            self.send_command(Command.Safe)
        elif new_mode == Mode.Full:
            self.send_command(Command.Full)
        elif new_mode == Mode.Off:
            self.send_command(Command.Power)
        else:
            raise ValueError('Invalid mode')

    def set_baud_rate(self, baud_rate):
        """
        Change the Baud rate of the Open Interface

        Args:
            baud_rate: a value from the BaudRate enum
        """

        self.send_command(Command.Baud, baud_rate.value)
        self.comm_device.baudrate = baud_rate.value

    def set_schedule(self, schedules=None):
        """
        Changes the cleaning schedule.

        To schedule a cleaning task for a given day of the week, pass
        the start times as a list of list containing the Weekday, the
        hour and the minute value. The hour value should use 00-23 and
        the minute value should use 00-59.

        Any Weekday that is not included in the list will have its
        schedule cleared.

        Examples:
            To schedule cleaning on Wednesday 3:00 pm and Saturday
            10:45 am, and clear schedules for all other days, use:
                set_schedule([[Weekday.Wednesday, 15, 0],
                              [Weekday.Saturday, 10, 45])

            To clear all scheduled tasks, use:
                set_schedule()
        """

        data_bytes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        weekday_index = {
            Weekday.Sunday: (1, 2),
            Weekday.Monday: (3, 4),
            Weekday.Tuesday: (5, 6),
            Weekday.Wednesday: (7, 8),
            Weekday.Thursday: (9, 10),
            Weekday.Friday: (11, 12),
            Weekday.Saturday: (13, 14)
        }
        if schedules is not None:
            for schedule in schedules:
                weekday = Weekday(schedule[0])
                if weekday >= 0 and weekday <= 6:
                    data_bytes[0] = data_bytes[0] | (1 << weekday)
                    hour_pos, minute_pos = weekday_index[schedule[0]]
                    data_bytes[hour_pos] = int(schedule[1]) % 24
                    data_bytes[minute_pos] = int(schedule[2]) % 60
        self.send_command(Command.Schedule, data_bytes)

    def set_clock(self, weekday=Weekday.Sunday, hour=0, minute=0):
        """
        Set system clock to a specific date and time.

        Args:
            weekday: a value from the Weekday enum
            hour: an integer value in the range of 0-23
            minute: an integer value in the range of 0-59
        """

        hour = int(hour) % 24
        minute = int(minute) % 60
        self.send_command(Weekday(weekday), [hour, minute])

    def drive(self, velocity=0, radius=0):
        """
        Drive the Roomba wheels.

        Args:
            velocity: the speed of moving (-500 to 500 mm/s)
            radius: the radius of turning (-2000 to 2000 mm)
        """

        velocity = min(max(int(velocity), -500), 500)
        radius = min(max(int(radius), -2000), 2000)

        data_bytes = [0, 0, 0, 0]
        if radius == 0 and velocity != 0:
            data_bytes[0], data_bytes[1] = velocity.to_bytes(2, 'big')
            data_bytes[2], data_bytes[3] = 0x80, 0x00
        elif velocity == 0 and radius > 0:
            data_bytes[0], data_bytes[1] = 0x01, 0xF4
            data_bytes[2], data_bytes[3] = 0x00, 0x01
        elif velocity == 0 and radius < 0:
            data_bytes[0], data_bytes[1] = 0x01, 0xF4
            data_bytes[2], data_bytes[3] = 0xFF, 0xFF
        else:
            data_bytes[0], data_bytes[1] = velocity.to_bytes(2, 'big')
            data_bytes[2], data_bytes[3] = radius.to_bytes(2, 'big')

        self.send_command(Command.Drive, data_bytes)

    def set_motor(self, main_brush=0, side_brush=0, vacuum=0):
        """
        Control the speed and direction of the motor parts.

        Args:
            main_brush: an integer of -127 to 127
            side_brush: an integer of -127 to 127
            vacuum: an integer of 0 to 127
        """

        pass

    def set_song(self, song_number, notes, durations):
        """
        Save a song into Roomba.

        Args:
            song_number: song index (0-4)
            notes: a list of integers ranging between 31 to 107.
            durations: a list of integers controlling the duration.
        
        The notes are from G (31) to B (107) with half note incremental.
        The middle C is 60. The C# is 61 and base B is 59, etc.
        Values outside of this range will be considered as rests.

        The duration is defined as N * 1/64 seconds where N is the
        specified interger value. So passing 32 will result in a note
        of 1/2 second.
        """

        MAX_NOTES_COUNT = 16

        if len(notes) != len(durations):
            raise ValueError('Length of notes and durations not match')
        if len(notes) == 0:
            raise ValueError('At least one note must be provided')
        if len(notes) > MAX_NOTES_COUNT:
            raise ValueError('Only %s notes allowed' % MAX_NOTES_COUNT)

        data = [song_number, len(notes)]
        data.extend(
            [v for zipped in zip(notes, durations) for v in zipped]
        )
        self.send_command(Command.Song, data)

    def play_song(self, song_number):
        """
        Play a song stored inside the Roomba (identified by its index).
        """

        song_number = max(0, min(song_number, 4))
        self.send_command(Command.Play, [song_number])
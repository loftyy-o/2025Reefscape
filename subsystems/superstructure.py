from enum import auto, Enum

from commands2 import Command, Subsystem, cmd
from wpilib import DriverStation, SmartDashboard

from subsystems.swerve import SwerveSubsystem


class Superstructure(Subsystem):
        
    class Goal(Enum):
        DEFAULT = auto()

    def __init__(self, drivetrain: SwerveSubsystem) -> None:
        super().__init__()

        self.drivetrain = drivetrain
        
        self._goal = self.Goal.DEFAULT
        self._last_goal = self.Goal.DEFAULT

    def periodic(self):
        if DriverStation.isDisabled():
            default_command = self.set_goal_command(self.Goal.DEFAULT)
            default_command.addRequirements(self)
            self.setDefaultCommand(default_command)

        self._last_goal = self._goal
        SmartDashboard.putString("Superstructure Goal", self._goal.name)
        
        match self._goal:
            case self.Goal.DEFAULT:
                self.drivetrain.set_desired_state(SwerveSubsystem.SubsystemState.DEFAULT)
        
    def _set_goal(self, goal: Goal) -> None:
        if goal is self._goal:
            return
        self._goal = goal
        
    def set_goal_command(self, goal: Goal) -> Command:
        return cmd.startEnd(
            lambda: self._set_goal(goal),
            lambda: self._set_goal(self.Goal.DEFAULT),
            self
        )

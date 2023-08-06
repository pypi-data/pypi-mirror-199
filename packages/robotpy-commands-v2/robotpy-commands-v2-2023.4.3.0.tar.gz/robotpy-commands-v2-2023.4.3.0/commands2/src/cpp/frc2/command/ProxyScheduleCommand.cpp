// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc2/command/ProxyScheduleCommand.h"

using namespace frc2;

ProxyScheduleCommand::ProxyScheduleCommand(
    std::span<std::shared_ptr<Command>> toSchedule) {
  SetInsert(m_toSchedule, toSchedule);
}

ProxyScheduleCommand::ProxyScheduleCommand(std::shared_ptr<Command> toSchedule) {
  std::shared_ptr<Command> v[] = {toSchedule};
  SetInsert(m_toSchedule, {v, 1});
}

void ProxyScheduleCommand::Initialize() {
  for (auto command : m_toSchedule) {
    Command_Schedule(command);
  }
}

void ProxyScheduleCommand::End(bool interrupted) {
  if (interrupted) {
    for (auto command : m_toSchedule) {
      command->Cancel();
    }
  }
}

void ProxyScheduleCommand::Execute() {
  m_finished = true;
  for (auto command : m_toSchedule) {
    m_finished &= !command->IsScheduled();
  }
}

bool ProxyScheduleCommand::IsFinished() {
  return m_finished;
}

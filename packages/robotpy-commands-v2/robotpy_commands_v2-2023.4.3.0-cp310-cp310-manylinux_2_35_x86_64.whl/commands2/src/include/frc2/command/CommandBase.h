// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <initializer_list>
#include <span>
#include <string>
#include <string_view>

#include <wpi/SmallSet.h>
#include <wpi/sendable/Sendable.h>
#include <wpi/sendable/SendableHelper.h>

#include "frc2/command/Command.h"

namespace frc2 {
/**
 * A Sendable base class for Commands.
 */
class CommandBase : public Command,
                    public wpi::Sendable,
                    public wpi::SendableHelper<CommandBase> {
 public:
  /**
   * Adds the specified Subsystem requirements to the command.
   *
   * The scheduler will prevent two commands that require the same subsystem
   * from being scheduled simultaneously.
   *
   * Note that the scheduler determines the requirements of a command when it
   * is scheduled, so this method should normally be called from the command's
   * constructor.
   *
   * @param requirements the Subsystem requirements to add
   */
  void AddRequirements(std::initializer_list<std::shared_ptr<Subsystem>> requirements);

  /**
   * Adds the specified Subsystem requirements to the command.
   *
   * The scheduler will prevent two commands that require the same subsystem
   * from being scheduled simultaneously.
   *
   * Note that the scheduler determines the requirements of a command when it
   * is scheduled, so this method should normally be called from the command's
   * constructor.
   *
   * @param requirements the Subsystem requirements to add
   */
  void AddRequirements(std::span<std::shared_ptr<Subsystem>> requirements);

  /**
   * Adds the specified Subsystem requirements to the command.
   *
   * The scheduler will prevent two commands that require the same subsystem
   * from being scheduled simultaneously.
   *
   * Note that the scheduler determines the requirements of a command when it
   * is scheduled, so this method should normally be called from the command's
   * constructor.
   *
   * @param requirements the Subsystem requirements to add
   */
  void AddRequirements(wpi::SmallSet<std::shared_ptr<Subsystem>, 4> requirements);

  /**
   * Adds the specified Subsystem requirement to the command.
   *
   * The scheduler will prevent two commands that require the same subsystem
   * from being scheduled simultaneously.
   *
   * Note that the scheduler determines the requirements of a command when it
   * is scheduled, so this method should normally be called from the command's
   * constructor.
   *
   * @param requirement the Subsystem requirement to add
   */
  void AddRequirements(std::shared_ptr<Subsystem> requirement);

  /**
   * Gets the Subsystem requirements of the command.
   *
   * @return the Command's Subsystem requirements
   */
  wpi::SmallSet<std::shared_ptr<Subsystem>, 4> GetRequirements() const override;

  /**
   * Sets the name of this Command.
   *
   * @param name name
   */
  void SetName(std::string_view name) override;

  /**
   * Gets the name of this Command.
   *
   * @return Name
   */
  std::string GetName() const override;

  /**
   * Gets the subsystem name of this Command.
   *
   * @return Subsystem name
   */
  std::string GetSubsystem() const;

  /**
   * Sets the subsystem name of this Command.
   *
   * @param subsystem subsystem name
   */
  void SetSubsystem(std::string_view subsystem);

  void InitSendable(wpi::SendableBuilder& builder) override;

 protected:
  CommandBase();
 public:
  wpi::SmallSet<std::shared_ptr<Subsystem>, 4> m_requirements;
};
}  // namespace frc2

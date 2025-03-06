from ..tag import Company, Skill, Tech

SKILLS: list[Skill] = [
  Company("Apple", ["(@)apple"]),

  # DESIGN
  # Tech("Sketch", ["sketch"], ""), many FPs, need to disambig.

  # MOBILE
  Tech("Swift", ["swift"]),
  Tech("AppKit", ["appkit"], "Framework"),
  Tech("SwiftUI", ["swiftui"], "Framework"),
  Tech("UIKit", ["uikit"], "Framework"),

  # OS
  Tech("iOS", ["ios"]),
  Tech("iPadOS", ["ipados"]),
  Tech("tvOS", ["tvos"]),
  Tech("watchOS", ["watchos"]),

  # DEVICES
  Tech("iMac", ["imac"]),
  Tech("iPad", ["ipad"]),
  Tech("iPhone", ["iphone"]),
  Tech("iWatch", ["iwatch"]),
]

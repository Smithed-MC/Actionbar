scoreboard objectives add smithed.actionbar.temp dummy
scoreboard objectives add smithed.actionbar.const dummy
scoreboard objectives add smithed.actionbar.priority dummy
scoreboard objectives add smithed.actionbar.freeze dummy

scoreboard players set $default.freeze smithed.actionbar.const 20
scoreboard players set $max.freeze smithed.actionbar.const 50
scoreboard players set $min.freeze smithed.actionbar.const 0

scoreboard objectives add smithed.actionbar.leaves minecraft.custom:minecraft.leave_game
scoreboard objectives add smithed.actionbar.scheduled dummy
scoreboard objectives add smithed.actionbar.math dummy
scoreboard objectives add smithed.actionbar.math2 dummy

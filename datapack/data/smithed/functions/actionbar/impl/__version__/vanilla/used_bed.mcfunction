advancement revoke @s only smithed:actionbar/__version__/vanilla/used_bed

# default
data modify storage smithed.actionbar:input message set value {json: '{"translate":"block.minecraft.bed.obstructed"}', priority: 'notification'}

# check hostiles
execute if entity @e[type=#smithed:actionbar/__version__/vanilla/hostiles,distance=..8] run data modify storage smithed:actionbar/storage temp.message.json set value '{"translate":"block.minecraft.bed.not_safe"}'

execute if entity @e[type=#smithed:actionbar/__version__/vanilla/neutral_hostiles,predicate=smithed:actionbar/__version__/vanilla/anger_time,distance=..8] run data modify storage smithed:actionbar/storage temp.message.json set value '{"translate":"block.minecraft.bed.not_safe"}'

# check time of day
execute if predicate smithed:actionbar/__version__/vanilla/no_sleep run data modify storage smithed.actionbar:input message.json set value '{"translate":"block.minecraft.bed.no_sleep"}'

# output ;)
function #smithed:actionbar/message

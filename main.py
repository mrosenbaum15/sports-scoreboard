from display import Display

myDisplay = Display(640, 22)
#myDisplay.draw_character('A',0,(100,0,0))
print('Drawing Top Line')
myDisplay.draw_line('ILLINI W', 0, (232, 74, 39))
print('Drawing Bottom Line')
myDisplay.draw_line('  24-7  ', 1, (19, 41, 75))
#print('Animating Border')
#myDisplay.animate_border((0,0,50))
myDisplay.draw_line('        ', 0, (19, 41, 75))
myDisplay.draw_line('        ', 1, (19, 41, 75))
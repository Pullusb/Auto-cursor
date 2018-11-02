# Auto-cursor
Blender Addon (2.79) - Make 3D cursor follow parented object/bone of active Grease Pencil layer
/!\ Once you have activate it, restart blender (it works with a background modal that is launched at startup)

**[Download latest](https://github.com/Pullusb/Auto-cursor/raw/master/auto_cursor.py)** (right click, save Target as) 

### Description:
Once you activate the `auto cursor` button the 3D cursor will follow your grease pencil layer's parent so you can draw over a 3D animation while keeping control on the depth of your line.

---

Select another parented layer and it will follow it (Here the animation is playing loop for demo purpose but usually you will change at a specific frame of your choice)

![change_target](https://github.com/Pullusb/images_repo/raw/master/AC_change_target.gif)

<br /><br /><br /><br /><br /><br />

---
You can choose to follow only the translation of an object instead of full LocRotScale by ticking `location only`.

![follow_loc_option](https://github.com/Pullusb/images_repo/raw/master/AC_follow_loc_option.gif)


<br /><br /><br /><br /><br /><br />

---
Demo where you can see the problem of drawing multiple animated frames on parented layers when cursor isn't moving.

![drawing_depth_example](https://github.com/Pullusb/images_repo/raw/master/AC_drawing_depth_example.gif)

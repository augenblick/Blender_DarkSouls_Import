
BEFORE INSTALLING, PLEASE NOTE!:
 - This add-on currently only works with Blender 2.8x
 - It currently only works with "Dark Souls - Prepare to Die Edition" (NOT REMASTERED!)
 - You MUST unpack your Dark Souls data with "Unpack Dark Souls for Modding" to access the game data.

=== INSTALLATION ===========================================
============================================================

(1)   In Blender, visit the Edit > Preferences > Add-ons menu.  From there, select "Install" and
navigate to the downloaded zip file (Blender will install the add-on directly from the zipped
file-- no need to unzip first).

(2)   The add-on should then appear in the Add-ons menu-- Be sure to enable it!


=== ADD-ON PREFERENCES =====================================
============================================================

After enabling the add-on, expand the add-on info panel 
and set the Add-on preferences for the three following items:

	- [.tpf filepath]
	- [.dds filepath]
	- ['Missing Texture' filepath] - (A simple UV grid exported from Blender is a good option.)
	
IMPORTANT!:  If you enter the paths manually, make sure the .tpf and .dds filepaths end with a backslash "\". 
Hover your mouse over any fields in Blender to see more info.

=== USE ====================================================
============================================================

After installation, look for a new "Dark Souls Import" tab in the 3D viewport toolbar (toggle with 'n')

Keep in mind that the directory set as the [.dds filepath] will gradually get larger and larger as more 
files are stored there.  This shouldn't noticeably affect the performance of the add-on, but you might 
clear the directory out from time to time just to save space.

=== KNOWN BUGS =============================================
============================================================

There are two major KNOWN bugs: 

 - Some textures cannot be found by the add-on.
 - Sometimes the add-on finds and applies the incorrect textures to meshes.

=== REPORTING NOVEL BUGS ===================================
============================================================

Please report bugs to the github (https://github.com/augenblick/Blender_DarkSouls_Import), or send
 an email to the developer (JimNateG@gmail.com).

When reporting novel bugs, please include relevant information regarding the problem.
	- Blender version
	- Operating System
	- Relevant console readout (In Blender go to 'Window' > 'Toggle System Console')
	- etc.

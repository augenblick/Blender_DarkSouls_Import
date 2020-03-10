1)   In Blender, visit the Edit > Preferences > Add-ons menu.  From there, select "Install" and navigate to the downloaded zip file (Blender will install the add-on directly from the zipped file-- no need to unzip first).

2)   The add-on should then appear in the Add-ons menu-- Be sure to enable it!

3)   After enabling, be sure to expand the add-on info and set the Add-on preferences for the three following items:
	- .tpf filepath: The directory containing .tpf files in the unpacked Dark Souls data
	- .dds filepath: Create a new directory or use an existing directory.  This is where the extracted .dds texture files will be stored.
	- 'Missing Texture' filepath: A path to a custom texture that will be used in cases where the add-on is unable to extract or find the required textures.  This can be any image file of your choosing(A simple UV grid exported from Blender is a good option.)

(Once set, these Add-on preferences should not have to be set on future sessions.)

After installation, Dark Souls importing mesh importing is accessible through a new "Dark Souls Import" tab in the 3D Viewport right-hand toolbar (toggle on/off with 'n').  You must be in object mode.

==========================================
This add-on is a work in progress!

When reporting bugs, please include relevant information regarding the problem.
	- Blender version
	- Operating System
	- Relevant console readout (In Blender go to 'Window' > 'Toggle System Console')
	- etc.

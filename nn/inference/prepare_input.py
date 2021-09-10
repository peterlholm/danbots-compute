from nn.inference.scan_generator.import_from_blender import convert_from_blender

def prepare_blender_input(infolder, outfolder):
    print("Preparing Blender Input")
    convert_from_blender(infolder, outfolder)
    return

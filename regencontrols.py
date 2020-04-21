import kle_lib.buttondefs
import pickle

print("Generating Controls Cache File...")
controls = kle_lib.buttondefs.getControls()
pickle.dump(controls, open("kle_lib/controlcache.p", 'wb'))
print("Done!")

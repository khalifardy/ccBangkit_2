from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
from tensorflow.python.framework import tensor_util
import os


app = FastAPI()

# load model

current_direktori = os.path.dirname(os.path.abspath(__file__))
model_path =os.path.join(current_direktori,'dietmodel.pb')
model = tf.saved_model.load(model_path)


@app.post("/prediksi")
async def predict(request:dict):

    try:

        inputs = {}
        for key, value in request.items():
            if isinstance(value, (int, float)):
                inputs[key] = tf.convert_to_tensor([value], dtype=tf.float32)
            else:
                inputs[key] = tf.convert_to_tensor([value],dtype=tf.string)
        print(model.signatures)

        output_tensor = model.signatures['serving_default'].outputs[0]
        output = model(inputs, training=False)[output_tensor]
        predictions = tensor_util.MakeNdarray(output.tensor_proto).tolist()
        respon = {"predictions":predictions}
    except Exception as e:
        respon = {"message":str(e)}

    

    return respon
"""
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
"""

import math

def calculate_angle(a,b,c):
    # abc npktaları [x,y,z] noktaları

    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]


    # dot product (iç çarpım) hesapla: ba · bc
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]

    # Vektörlerin büyüklüklerini hesapla
    magnitude_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    # Kosinüs açısını hesapla
    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

    # Açı hesapla ve dereceye çevir
    angle = math.degrees(math.acos(cosine_angle))

    return angle
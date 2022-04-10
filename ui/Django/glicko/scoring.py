import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as control


def scoring_fuzzy_logic(z, y, x, dist):
    accel_z = control.Antecedent(np.arange(0, 3, 0.5), "Z")
    accel_y = control.Antecedent(np.arange(0, 3, 0.5), "Y")
    accel_x = control.Antecedent(np.arange(0, 3, 0.5), "X")
    distance = control.Antecedent(np.arange(0, 1500, 100), "D")
    safety = control.Consequent(np.arange(0, 1, 0.1), "S")

    accel_z["VL"] = fuzz.gaussmf(accel_z.universe, 0.03085, -0.000936)
    accel_z["ML"] = fuzz.gaussmf(accel_z.universe, 0.0816, 0.2728)
    accel_z["MH"] = fuzz.gaussmf(accel_z.universe, 0.116, 0.628)
    accel_z["VH"] = fuzz.gaussmf(accel_z.universe, 0.543, 1.783)

    accel_x["VL"] = fuzz.gaussmf(accel_x.universe, 0.2898, 0)
    accel_x["ML"] = fuzz.gaussmf(accel_x.universe, 0.114, 0.5166)
    accel_x["N"] = fuzz.gaussmf(accel_x.universe, 0.156, 1.164)
    accel_x["MH"] = fuzz.gaussmf(accel_x.universe, 0.0831, 1.543)
    accel_x["VH"] = fuzz.gaussmf(accel_x.universe, 0.51, 2.477)

    accel_y["VL"] = fuzz.gaussmf(accel_y.universe, 0.1699, 0)
    accel_y["ML"] = fuzz.gaussmf(accel_y.universe, 0.128, 0.5001)
    accel_y["MH"] = fuzz.gaussmf(accel_y.universe, 0.129, 0.9798)
    accel_y["VH"] = fuzz.gaussmf(accel_y.universe, 0.823, 2.429)

    distance["C"] = fuzz.trapmf(distance.universe, [-743, -143, 160, 272.4])
    distance["N"] = fuzz.trapmf(distance.universe, [138, 445, 730.3, 871])
    distance["F"] = fuzz.trapmf(distance.universe, [776, 893, 1570, 2100])

    safety["cautious"] = fuzz.trimf(safety.universe, [-0.417, 0, 0.2178])
    safety["normal"] = fuzz.trimf(safety.universe, [0.158, 0.5, 0.6218])
    safety["risky"] = fuzz.trimf(safety.universe, [0.5544, 0.8535, 1.225])

    rule1 = control.Rule(accel_z["VH"] & distance["C"], safety["risky"])
    rule2 = control.Rule(accel_z["MH"] & distance["C"], safety["risky"])
    rule3 = control.Rule(accel_z["MH"] & distance["N"], safety["normal"])
    rule4 = control.Rule(accel_z["ML"] & distance["N"], safety["normal"])
    rule5 = control.Rule(accel_z["VL"] & distance["N"], safety["cautious"])
    rule6 = control.Rule(accel_z["ML"] & distance["F"], safety["cautious"])
    rule7 = control.Rule(accel_z["VL"] & distance["F"], safety["cautious"])
    rule8 = control.Rule(accel_x["VL"] & distance["F"], safety["cautious"])
    rule9 = control.Rule(accel_x["ML"] & distance["F"], safety["cautious"])
    rule10 = control.Rule(accel_x["VL"] & distance["N"], safety["cautious"])
    rule11 = control.Rule(accel_x["ML"] & distance["N"], safety["normal"])
    rule12 = control.Rule(accel_x["VL"] & distance["C"], safety["normal"])
    rule13 = control.Rule(accel_x["ML"] & distance["C"], safety["normal"])
    rule14 = control.Rule(accel_x["VL"] & distance["N"], safety["cautious"])
    rule15 = control.Rule(accel_x["N"] & distance["N"], safety["normal"])
    rule16 = control.Rule(accel_x["N"] & distance["C"], safety["risky"])
    rule17 = control.Rule(accel_x["N"] & distance["F"], safety["cautious"])
    rule18 = control.Rule(accel_x["MH"] & ~distance["C"], safety["normal"])
    rule19 = control.Rule(accel_x["MH"] & distance["C"], safety["risky"])
    rule20 = control.Rule(accel_x["VH"] & distance["C"], safety["risky"])
    rule21 = control.Rule(accel_x["VH"] & distance["N"], safety["risky"])
    rule22 = control.Rule(accel_x["VH"] & distance["F"], safety["normal"])
    rule23 = control.Rule(accel_y["VL"] & distance["N"], safety["cautious"])
    rule24 = control.Rule(accel_y["VL"] & distance["F"], safety["cautious"])
    rule25 = control.Rule(accel_y["VL"] & distance["C"], safety["cautious"])
    rule26 = control.Rule(accel_y["ML"] & distance["C"], safety["cautious"])
    rule27 = control.Rule(accel_y["ML"] & distance["N"], safety["cautious"])
    rule28 = control.Rule(accel_y["ML"] & distance["F"], safety["cautious"])
    rule29 = control.Rule(accel_y["MH"] & distance["C"], safety["risky"])
    rule30 = control.Rule(accel_y["MH"] & distance["N"], safety["normal"])
    rule31 = control.Rule(accel_y["MH"] & distance["F"], safety["cautious"])
    rule32 = control.Rule(accel_y["VH"] & distance["C"], safety["risky"])
    rule33 = control.Rule(accel_y["VH"] & distance["N"], safety["risky"])
    rule34 = control.Rule(accel_y["VH"] & distance["F"], safety["cautious"])
    rule35 = control.Rule(
        accel_z["VH"] & accel_x["VH"] & accel_y["VH"], safety["risky"]
    )
    rule36 = control.Rule(
        accel_z["VH"] & accel_x["MH"] & accel_y["VH"], safety["risky"]
    )
    rule37 = control.Rule(accel_z["VH"] & accel_x["N"] & accel_y["VH"], safety["risky"])
    rule38 = control.Rule(
        accel_z["VH"] & accel_x["ML"] & accel_y["VH"], safety["normal"]
    )
    rule39 = control.Rule(
        accel_z["VH"] & accel_x["VL"] & accel_y["VH"], safety["normal"]
    )
    rule40 = control.Rule(
        accel_z["VH"] & ~accel_x["VH"] & accel_y["MH"], safety["normal"]
    )
    rule41 = control.Rule(
        accel_z["VH"] & ~accel_x["MH"] & accel_y["MH"], safety["normal"]
    )
    rule42 = control.Rule(
        accel_z["VH"] & accel_x["VH"] & accel_y["MH"], safety["risky"]
    )
    rule43 = control.Rule(
        accel_z["MH"] & accel_x["VH"] & accel_y["VH"], safety["risky"]
    )
    rule44 = control.Rule(accel_z["MH"] & accel_x["MH"], safety["risky"])
    rule45 = control.Rule(
        accel_z["MH"] & accel_x["N"] & accel_y["MH"], safety["normal"]
    )
    rule46 = control.Rule(~accel_z["VH"] & accel_x["N"], safety["normal"])
    rule47 = control.Rule(
        ~accel_z["VH"] & accel_x["N"] & ~accel_y["VH"], safety["normal"]
    )
    rule48 = control.Rule(
        accel_z["ML"] & accel_x["N"] & accel_y["ML"], safety["cautious"]
    )
    rule49 = control.Rule(accel_x["ML"] & ~accel_y["VH"], safety["cautious"])
    rule50 = control.Rule(~accel_z["VH"] & accel_x["ML"], safety["cautious"])
    rule51 = control.Rule(~accel_z["VH"] & accel_x["VL"], safety["cautious"])
    rule52 = control.Rule(
        accel_z["VH"] & accel_x["VL"] & ~accel_y["VH"], safety["cautious"]
    )

    rules = []
    for i in range(1, 53):
        rules.append(eval("rule" + str(i)))

    safety_ctrl = control.ControlSystem(rules)

    safety_sim = control.ControlSystemSimulation(safety_ctrl)
    safety_sim.input["Z"] = z
    safety_sim.input["Y"] = y
    safety_sim.input["X"] = x
    safety_sim.input["D"] = dist

    safety_sim.compute()
    return safety_sim.output["S"]


# async def main():
#     print(datetime.datetime.now())
#     async with aiofiles.open("longer_trip1.csv", mode="r") as csv_file:
#         scored = 0

#         counter = 0
#         async for row in csv_file:
#             if counter == 0:
#                 counter += 1
#                 continue
#             else:
#                 row = row.split(",")
#                 scored += await scoring_fuzzy_logic(
#                     float(row[3]), float(row[2]), float(row[1]), float(row[4])
#                 )
#                 counter += 1

#     print(round(scored) / counter, 4)
#     print("done", datetime.datetime.now())


# loop = asyncio.get_event_loop()
# runner = loop.run_until_complete(main())


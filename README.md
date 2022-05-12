# CalEW
Calculate Wet Bulb Temperature from temperture, rh, and pressure



使用干湿平衡公式，通过气温、相对湿度、气压，计算平衡时的湿球温度。

输入：气温（摄氏度），相对湿度（%），气压（百帕）
输出：平衡时饱和水汽压，平衡时湿球温度
方法：首先计算平衡时的饱和水汽压，再通过饱和水汽压计算得到湿球温度
环境：Python3.8， Linux

已知问题：
1）冰、液分段导热系数A会导致湿球温度在0度附近时有跳跃现象，进而导致计算时不收敛。这个误差通常较少出现，若出现，一般误差在0.2度以内；
2）出现情形1）时，可以通过二分法计算收敛区间内的值，但是收敛速度会变慢（只慢一点点）

Using the wet and dry balance formula, the wet bulb temperature at equilibrium is calculated by air temperature, relative humidity, and air pressure.

Inputs: air temperature (degrees Celsius), relative humidity (%), air pressure (hPa)
Output: Saturated water vapor pressure at equilibrium, wet bulb temperature at equilibrium
Method: The saturated water vapor pressure at equilibrium is calculated first, and then the wet bulb temperature is obtained by calculating the saturated water vapor pressure

Known issues:
1) Ice and liquid segmented thermal conductivity A will cause the wet bulb temperature to jump when it is near 0 degrees, which will lead to non-convergence during calculation. This error usually occurs less frequently, and if it does, the general error is within 0.2 degrees;
2) In case 1), the value in the convergence interval can be calculated by dichotomy, but the convergence rate will be slower (only a little slower)

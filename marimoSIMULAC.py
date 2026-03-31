import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full", app_title="pySIMULAC")


@app.cell
def _():
    # /// script
    # requires-python = ">=3.10"
    # dependencies = [
    #   "marimo",
    #   "pandas",
    #   "numpy",
    # ]
    # ///
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from math import pow, pi, sqrt
    from dataclasses import dataclass
    from enum import Enum
    from typing import ClassVar, List
    from collections import namedtuple
    import pandas as pd
    from math import sqrt, pi
    import numpy as np

    return ClassVar, Enum, List, dataclass, mo, namedtuple, pd, pi, sqrt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1 Parámetros de la Faena <br>

     En el módulo 1 *Parámetros de la Faena* se definen las características del bosque y la planificacion de los tiempos de la faena. Este módulo está compuesto por 4 sub-módulos:<br>
     - *Descrición del Rodal*<br>
     - *Programación del Trabajo*<br>
     - *Transporte Secundario*<br>
     - *Costos indirectos*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>
    ## 1.1 Descripcion del Rodal <br>
    En este módulo se ingresan las características dasométricos del rodal.<br>

    *Inputs*: <br>
    + $N$: Número de árboles por hectárea $(n^{1}ha^{-1})$. <br>
    + $DAPm$: Promedio de los diámetros a la altura del pecho de árboles del rodal $(cm)$. <br>
    + $Hm$: Altura media de los árboles $(m)$. <br>
    + $STC$: Superficie Total a Cosechar $(ha)$. <br>
    <br>
    *Outputs*: <br>
    - $DeA :$ Distancia entre Árboles (m)
      - Donde $DeA = \sqrt{\frac{10000}{N}}$
    + $Vm :$ Volumen del árbol medio (${m^3}$)
      - Donde $Vm$ =  Volumen Smalian en base al $DAPm$, $Hm$ y asumiendo un ahusamiento lineal de 1 ($cm^{1}m^{-1}$)<br>
    + $V :$ Volumen por hectárea (${m^3}{ha^{-1}}$) <br>
      - Donde $V = Vm *N$ <br>
    + $VTC :$ Volúmen Total a Cosechar ($m^3$) <br>
      - Donde $VTC= V * STC$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    N_number = mo.ui.number(label="Número de árboles por hectárea ", value= 450)
    DAP_number = mo.ui.number(label="Diámetro a la Altura del Pecho ", value=38.1687)
    Hm_number = mo.ui.number(label="Altura del árbol medio ", value= 12)
    STC_number = mo.ui.number(label="Superficie total a cosechar", value=50.2)
    return DAP_number, Hm_number, N_number, STC_number


@app.cell(hide_code=True)
def _(DAP_number, Hm_number, N_number, STC_number, smalian, sqrt):

    # parámetros
    N = round(N_number.value)
    DAP = DAP_number.value
    Hm =  Hm_number.value # (m)
    STC =STC_number.value  # ha)


    # cálculos
    DeA = sqrt(10000 / N)  # (m)
    vm = smalian(DAP, Hm)  # (m3)
    V = vm * N  # (m3/ha)
    VTC = V * STC  #Volumen Total Cosecha
    return DeA, V, VTC, vm


@app.cell
def _(pi):
    def smalian(dap:float, largo:float):
        """Volumen Smalian considerando en base al DAPm, Hm(largo) y considerando un ahusamiento lineal de 1 cm por metro"""
        ahusamiento = 1
        dmayor = dap - 1 # Considerando que el dap se mide a 1.3 m y hay unapérdida por tocón de 0.3m
        dmenor = dmayor - (largo * ahusamiento)
        return (pi/40000 * ((dmayor**2 + dmenor**2)/2)) * largo


    return (smalian,)


@app.cell(hide_code=True)
def _(DeA, V, VTC, mo, vm):
    output_m11 = mo.md(rf"*Output Descripción del Rodal:*<br>-La distancia entre arboles ($DeA$), es igual a **{DeA:.1f} $m$**<br>     - El volumen del árbol medio ($Vm$), es igual a **{vm:.1f} $m^{3}$**<br>- El volumen por hectárea ($V$), es igual a **{V:.1f} $m^{3}ha⁻¹$**<br>- El volumen total a cosecha ($VTC$), es igual a **{VTC:.1f} $m^{3}$**<br>")
    return (output_m11,)


@app.cell(hide_code=True)
def _(DAP_number, Hm_number, N_number, STC_number, mo):
    panel_inputs = mo.md(f"""
    | Parámetro | Valor | Unidad |
    |------------|---------|-------|
    | N | {N_number} | $(N)$|
    | DAP | {DAP_number} | $(cm)$ |
    | Hm | {Hm_number} | $(m)$ |
    | STC | {STC_number} | $(ha)$ |
    """)

    mo.vstack([mo.md("Panel *Descripción del Rodal :* "),panel_inputs])
    return


@app.cell
def _(output_m11):
    output_m11
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br>
    ## 1.2 Programación del Trabajo
    En este submódulo *Programación del Trabajo* se definen los horarios y fechas planificadas del sistema productivo, es decir, de los subsistemas *Volteo, Madereo, Procesado y Carguío*<br>
    + Inputs :<br>
     + $HD :$ Horas planificadas por jornada laboral (${{hrpl}}^{1}{{día}}^{{-1}}$)
     + $DM :$ Días planificados por trabajar al mes (${{días}}^{1}mes^{{-1}}$)
     + $MA :$ Meses planificdos por trabajar al año ($mes^{1}años^{{-1}}$)
    <br>
    + Outputs :
     + $hrpl_{mes} :$ Horas planificadas mensuales
       + Donde $hrpl_{mes} = HD * DM$
     + $hrpl_{año} :$ Horas
       + Donde $hrpl_{año} = hrpl_{mes} * MA$
    """)
    return


@app.cell(hide_code=True)
def _(DM_number, HD_number, MA_number):
    """1.2 Programacion del trabajo"""
    #Esta es la programación de la jornada laboral válida para los subsistemas volteo, madereo, procesado y carguío
    # Inputs
    HD = round(HD_number.value)  # horas diarias
    DM = round(DM_number.value)  # días al mes
    MA = round(MA_number.value)# meses al año
    # Outputs
    hrpl_m = round(HD * DM)
    hrpl_a = hrpl_m * MA
    return DM, HD, hrpl_a, hrpl_m


@app.cell(hide_code=True)
def _(mo):
    HD_number = mo.ui.number(label="Horario laboral diario (hrs)", value=10)
    DM_number = mo.ui.number(label="Días que se trabaja al mes (días)", value=30)
    MA_number = mo.ui.number(label="Meses al año (meses)", value=12)

    inputs_m12 = mo.md(f"""
    | Parámetro |Valor  |
    |------------|---------|
    | HD | {HD_number} |
    | DM | {DM_number} |
    | MA | {MA_number} |
    """)
    mo.vstack([mo.md("Inputs ***Programación del trabajo :***"),
              inputs_m12])
    return DM_number, HD_number, MA_number


@app.cell
def _(hrpl_a, hrpl_m, mo):
    m12_output = [mo.md(rf"*Output*<br> Horas planificadas mensuales (${{hrpl}}_{{mes}}$): **{hrpl_m}** <br>Horas planificadas anuales (${{hrpl}}_{{año}}$) : **{hrpl_a}**")]
    m12_output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br>

    ## 1.3 Transporte Secundario <br>
    >En este submódulo se planifican los tiempos del transporte secundario, el cual funciona de forma paralela al sistema productiv.o<br>
    - Inputs :<br>
      - $HDT:$ Horas Diarias Transporte ($hrpl^1{{día}}^{{-1}}$).<br>
      - $DST :$ Días a la Semana Transporte ($días^1{{semana}}^{{-1}}$).<br>
      - $CSRP :$ Capacidad Semanal de Recepcion en Planta ($m^3{{semana}}^{{-1}}$).<br>
      - $Dist :$ Distancia entre el punto de carga del camión y el aserradero o centro de recepción $(km)$.<br>
      - $CCC :$ Capacidad de carga del camion (m$^3$).
      - $TC :$ Tiempo de carga del camión $(min)$.
      - $TD :$ Tiempo de descarga del camión $(min)$.
      - $VCC :$ Velocidad del Camion Cargado ($km^1{{hora}}^{{-1}}$).<br>
      - $VCV :$ Velocidad del Camion Vacío ($km^1{{hora}}^{{-1}}$).<br>
    - Output<br>
      - $TC_{hora}$ Tiempo de Carga del camión en horas $(hora)$.
        - Donde $TC_{hora} = TC/60$
      - $TD_{hora}$ Tiempo de Descarga del camión en horas $(hora)$.
        - Donde $TD_{hora} = TD/60$
      - $PC :$ Productividad del Camion (${m}^{3}{hrpr^{-1}}$).<br>
        - Donde $PC = (\frac{CCC_{[m^3]}}{\frac{Dist_{[km]}}{VCC_{[km/hr]}}+\frac{Dist_{[km]}}{VCV_{[km/hr]}}+{TC_{hora[hora]}+{TD_{hora[hora]}}}})$
      <br>
    """)
    return


@app.cell
def _(mo):
    HDT_number = mo.ui.number(label="Horario diario de trabajo del transporte", value = 10)
    DST_number = mo.ui.number(label=" Días a la Semana de Transporte ", value = 7)
    Dist_transporte_number = mo.ui.number(label="Distancia Transporte Secundario ", value =1)
    CSRP_number = mo.ui.number(label=(f"Capacidad semanal de recepción en planta "), value = 5000 )
    CCC_number = mo.ui.number(label="Capacidad de carga del camión ", value = 2000 )
    VCC_number = mo.ui.number(label="Velocidad Camión Cargado ", value = 80 ) 
    VCV_number = mo.ui.number(label="Velocidad Camión Vacío ", value = 120 )
    TC_number = mo.ui.number(label="Tiempo Carga", value = 60)
    TD_number = mo.ui.number(label="Tiempo Descarga", value = 60)
    return (
        CCC_number,
        CSRP_number,
        DST_number,
        Dist_transporte_number,
        HDT_number,
        TC_number,
        TD_number,
        VCC_number,
        VCV_number,
    )


@app.cell
def _(
    CCC_number,
    CSRP_number,
    DST_number,
    Dist_transporte_number,
    HDT_number,
    TC_number,
    TD_number,
    VCC_number,
    VCV_number,
):
    """Transporte Secundario"""

    # Inputs
    HDT = HDT_number.value
    DST = DST_number.value
    Dist_transporte = Dist_transporte_number.value
    CSRP = CSRP_number.value # Capacidad semanal de recepción en planta
    CCC = CCC_number.value
    VCC = VCC_number.value
    VCV = VCV_number.value
    TC = TC_number.value
    TD = TD_number.value
    # Outputs
    TC_hora = TC/60
    TD_hora = TC/60
    PT = (CCC /  ((Dist_transporte / VCC) + (Dist_transporte/ VCV) + TC_hora + TD_hora)) # esto sería en horas productivas, sin considerar la disponibilidad mecánica del transporte
    recepcion_planta_m3hrpl = (CSRP / (DST * HDT))
    return HDT, PT, TC, recepcion_planta_m3hrpl


@app.cell
def _(
    CCC_number,
    CSRP_number,
    DST_number,
    Dist_transporte_number,
    HDT_number,
    PT,
    TC,
    TC_number,
    TD_number,
    TRANSPORTE_A,
    VCC_number,
    VCV_number,
    mo,
    recepcion_planta_m3hrpl,
):
    output13 = [
        "Output:",
        mo.md(rf"Tiempo Carga Camión en Horas ($hora$) = **{TC / 60:.1f}** "),
        mo.md(rf"Tiempo Descarga Camión en Horas ($hora$) = **{TC / 60:.1f}** "),
        mo.md(
            f"Productividad Camión ($m^{{3}}\\,hrpl^{{-1}}$) = **{PT*TRANSPORTE_A.disponibilidad:.1f}**"
        ),
        mo.md(
            f"Recepción en planta ($m^{{3}}\\,hrpl^{{-1}}$) = **{recepcion_planta_m3hrpl:.1f}**"
        )
    ]

    b = mo.vstack([
        mo.md("**Inputs :**"),
        HDT_number,
        DST_number,
        Dist_transporte_number,
        CSRP_number, 
        CCC_number,
        VCC_number, 
        VCV_number, 
        TC_number, 
        TD_number, 
        output13
    ], align='start')

    inputs_m13 = mo.md(f"""
    | Parámetro | Valor | Unidad |
    |------------|---------|-----|
    | HDT | {HDT_number} | $(horas^1día^{{-1}})$ |
    | DST | {DST_number} | $(días)$ |
    | DIST | {Dist_transporte_number} | $(km)$ |
    | CSRP | {CSRP_number} | $(m^3semana^{{-1}})$ |
    | CCC| {CCC_number} | $(m^3)$ |
    | VCC | {VCC_number} | $(km^1hr^{{-1}})$ |
    | VCV | {VCV_number} | $(km^{1}hr^{{-1}})$ |
    | TC | {TC_number} | $(minutos)$ |
    | TD | {TC_number} | $(minutos)$ |
    """)

    mo.vstack([mo.md("Inputs del submódulo ***Transporte Secundario***"),
               inputs_m13,
               mo.md("<br> Outputs del submódulo ***Transporte Secundario***"),
               output13])
    return


@app.cell
def _(mo):
    mo.md(r"""
    <br>
    ## 1.4 Costos indirectos y otros costos <br>
    - $Inputs :$<br>
     - $CI_{admin}:$ Costos Administrativos ($$^{1}mes^{-1})$
     - $CI_{implemen} :$ Costos de implementacion ($$^{1}mes^{-1})$
     - $CI_{superv} :$ Costos de Supervicion ($$^{1}mes^{-1}) :$
     - $precio_{combustible}$ ($$^{1}lt^{-1}) :$
     - $BS :$ Beneficios Sociales. Representa el porcentaje del sueldo destinado a las prestaciones <br>
    - *Outputs*<br>
     - $CI_{totales} :$ Costos indirectos totales ($$^{1}hrpl^{-1}$).
        - Donde $CI_{totales} = \frac{(CI_{admin} + CI_{implemen} + CI_{suerpv})}{hrpl_{mes}}$ <br>
    <br>
    """)
    return


@app.cell
def _(mo):
    ci_administracion_number = mo.ui.number(label="Costos Indirectos de Administración ", value = 1000)
    ci_implementacion_number = mo.ui.number(label="Costos Indirectos de Implementación  ", value = 1000)
    ci_supervision_number = mo.ui.number(label="Costos Indirectos de Supervisión", value = 1000)
    precio_combustible_number = mo.ui.number(label="Precio del Combustible ", value = 0.86)
    beneficios_sociales_number = mo.ui.number(label="Porcentaje de Beneficios Sociales ", value = 0.2)
    return (
        beneficios_sociales_number,
        ci_administracion_number,
        ci_implementacion_number,
        ci_supervision_number,
        precio_combustible_number,
    )


@app.cell
def _(
    beneficios_sociales_number,
    ci_administracion_number,
    ci_implementacion_number,
    ci_supervision_number,
    mo,
    precio_combustible_number,
):
    input14 =  [mo.md("*Inputs:*"),
                ci_administracion_number,
                ci_implementacion_number,
                ci_supervision_number,
               precio_combustible_number,
               beneficios_sociales_number]

    mo.md(f"""
    | Parámetro/Descripción     | Valor |Unidad|
    |-----------|-------|------|
    |$CI_{{admin}}$| {ci_administracion_number}| $(\$^{1}{{mes}}^{{-1}})$ |
    |$CI_{{implem}}$| {ci_implementacion_number} |  $(\$^{1}{{mes}}^{{-1}})$ |
    |$CI_{{Superv}}$| {ci_supervision_number} |  $(\$^{1}{{mes}}^{{-1}})$ |
    | ${{PrecComb}}$ | {precio_combustible_number}| $( \$^1{{lt}}^{{-1}})$ |
    | ${{BenSoc}}$ |{beneficios_sociales_number}| $(\%, decimal)$

    """)
    return (input14,)


@app.cell
def _(input14, mo):

    mo.hstack([
        mo.vstack(i for i in input14)
    ])
    return


@app.cell
def _(
    DM,
    HD,
    beneficios_sociales_number,
    ci_administracion_number,
    ci_implementacion_number,
    ci_supervision_number,
    mo,
    precio_combustible_number,
):
    ci_administracion = ci_administracion_number.value
    ci_implementacion = ci_implementacion_number.value
    ci_supervision = ci_supervision_number.value
    precio_combustible = precio_combustible_number.value
    beneficios_sociales = beneficios_sociales_number.value # (porcentaje)

    ci_totales = (( ci_administracion + ci_implementacion + ci_supervision)/(DM * HD))
    mo.vstack([mo.md(rf"Los Costos Indirectos Totales son **{ci_totales} $$^{{1}}hrpl^{{-1}}$**")])
    return beneficios_sociales, precio_combustible


@app.cell
def _(mo):
    mo.md(r"""
    <br><br>
    # 2 Maquinaria Disponible
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Clase MAQUINA <br>
    En la clase *Maquina* se estima el costo horario de cada máquina usando una versión simplificada de la metodología de costeo de *Brinker et al 2002*. El costo horario de una máquina considera el horario laboral planificado y la disponibilidad mecánica, más no considera efectos de falta de producción como consecuencia de la formación de cuellos de botella en la cadena productiva.<br>
    > Las diferencias respecto del texto de referencia son las siguientes:<br>
    - En *Brinker et al 2002* los costos de mano de obra y beneficios sociles se incluyen dentro de los costos variables. En cambio, aquí ambos tipos de costo se calculan de forma independiente.
    - En esta clase, el costo de combustible ($/hr) se calcula solamente en función del consumo esperado y del costos del combustible, a diferencia de *Brinker et al 2002* quién también incluye la potencia del motor *(hp)* como variable independiente.
    """)
    return


@app.cell
def _(beneficios_sociales, dataclass, hrpl_a, hrpl_m, precio_combustible):
    @dataclass(slots=True)
    class Maquina:
        nombre: str
        tipo_maquina: str
        productividad_maquina: float  # (m3/hrpr)
        inversion_inicial: float
        vida_util: float
        disponibilidad: float  # decimal
        factor_reventa: float  # decimal
        factor_reparacion: float  # decimal
        interes: float # decimal
        impuestos: float # decimal
        seguros: float # decimal
        uso_anual_planificado: float
        consumo_combustible: float  # lt/hrpr
        factor_lubricantes: float  # decimal
        sueldo_operador: float  # clp/mes

        def __post_init__(self):
            if not (0 < self.disponibilidad <= 1):
                raise ValueError(
                    "disponibilidad debe ser mayor a 0 y no mayor a 1"
                )
            if not (0 < self.factor_reventa <= 1):
                raise ValueError(
                    "factor_reventa debe ser mayor a 0 y no mayor a 1"
                )
            if not (0 < self.factor_reparacion <= 1):
                raise ValueError(
                    "factor_reparacion debe ser mayor a 0 y no mayor a 1"
                )
            if not (0 < self.factor_lubricantes <= 1):
                raise ValueError(
                    "factor_lubricantes debe ser mayor a 0 y no mayor a 1"
                )

        @property
        def valor_reventa(self) -> float:
            """Calcula el valor de reventa de la Maquina ($)"""
            return self.inversion_inicial * self.factor_reventa

        @property
        def depreciacion_anual(self) -> float:
            """Devuelve la depreciacion anual de una Maquina ($/año)"""
            return (self.inversion_inicial - self.valor_reventa) / self.vida_util

        @property
        def ima(self) -> float:
            """Devuelve la inversion media anual ($/año)"""
            return (
                (
                    (self.inversion_inicial - self.valor_reventa)
                    * (self.vida_util + 1)
                )
                / (2 * self.vida_util)
            ) + self.valor_reventa

        # COSTOS FIJOS
        @property
        def inversion_impuestos_seguros(self) -> float:
            return self.ima * (self.interes + self.impuestos + self.seguros)

        @property
        def costo_anual_propiedad(self) -> float:
            """Calcula el costo anual de propiedad ($/año)"""
            return self.inversion_impuestos_seguros + self.depreciacion_anual

        @property
        def horas_productivas_anuales(self) -> float:
            return hrpl_a * self.disponibilidad

        @property
        def cfm_hrpr(self) -> float:
            """Costo fijo de la Maquina por hora productiva $/hrpr"""
            return self.costo_anual_propiedad / self.horas_productivas_anuales

        @property
        def cfm_hrpl(self) -> float:
            """Costo fijo de la Maquina por hora planificada $/hrpl"""
            return self.costo_anual_propiedad / self.uso_anual_planificado

        # COSTOS VARIABLES
        @property
        def costos_combustibles(self) -> float:
            "costos en $ / hrpr"
            return self.consumo_combustible * precio_combustible

        @property
        def costos_lubricantes(self) -> float:
            "costos en $ / hrpr"
            return self.factor_lubricantes * self.costos_combustibles

        @property
        def costos_mantencion_reparacion(self) -> float:
            "costos en $ / hrpr"
            return (
                self.factor_reparacion * self.depreciacion_anual
            ) / 3600

        @property
        def cvm_hrpr(self) -> float:
            "Costo variable Máquina expresado en horas productivas"
            return (
                self.costos_combustibles
                + self.costos_lubricantes
                + self.costos_mantencion_reparacion
            )

        @property
        def cvm_hrdi(self) -> float:
            "Costo variable máquina expresado en horas disponibles"
            return self.cvm_hrpr * self.disponibilidad

        # COSTOS MANOS DE OBRA
        @property
        def cmom_hrpl(self) -> float:
            """Costo horario neto de unidad de mano de obra """
            return ((self.sueldo_operador / hrpl_m) * (1+beneficios_sociales))


    return (Maquina,)


@app.cell
def _(ClassVar, Enum, List, Maquina, dataclass):
    class TipoVolteo(Enum):
        MOTOSIERRA = "Motosierra"
        FELLERBUNCHER = "Fellerbuncher"
        HARVESTER = "Harvester"


    @dataclass(slots=False)
    class Volteo(Maquina):
        registro: ClassVar[List["Volteo"]] = []
        TIPOS_VALIDOS = {t.value for t in TipoVolteo}

        def __post_init__(self):
            super().__post_init__()
            Volteo.registro.append(self)
            if self.tipo_maquina not in self.TIPOS_VALIDOS:
                raise ValueError(
                    f"tipo_maquina '{self.tipo_maquina}' no válido para Volteo. "
                    f"Opciones: {self.TIPOS_VALIDOS}"
                )

    return (Volteo,)


@app.cell
def _(ClassVar, Enum, List, Maquina, dataclass):
    class TipoMadereo(Enum):
        SKIDDER_GARRA = "Skidder-Garra"
        SKIDDER_HUINCHA = "Skidder-Huincha"
        CAMION_AUTOCARGABLE = "Camion-Autocargable"
        TRACTOR = "Tractor"


    @dataclass(slots=False)
    class Madereo(Maquina):
        registro: ClassVar[
            List["Madereo"]
        ] = []  # para llevar la cuenta (se inicialia abajo)
        TIPOS_VALIDOS = {t.value for t in TipoMadereo}

        def __post_init__(self):
            Madereo.registro.append(self)
            super().__post_init__()
            if self.tipo_maquina not in self.TIPOS_VALIDOS:
                raise ValueError(
                    f"tipo_maquina '{self.tipo_maquina}' no válido para Madereo. "
                    f"Opciones: {self.TIPOS_VALIDOS}"
                )

    return (Madereo,)


@app.cell
def _(ClassVar, Enum, List, Maquina, dataclass):
    class TipoProcesado(Enum):
        MOTOSIERRA = "Motosierra"
        PROCESADOR = "Procesador"


    @dataclass(slots=False)
    class Procesado(Maquina):
        registro: ClassVar[
            List["Procesado"]
        ] = []  # para llevar la cuenta (se inicialia abajo)
        TIPOS_VALIDOS = {t.value for t in TipoProcesado}

        def __post_init__(self):
            super().__post_init__()
            Procesado.registro.append(self)
            if self.tipo_maquina not in self.TIPOS_VALIDOS:
                raise ValueError(
                    f"tipo_maquina '{self.tipo_maquina}' no válido para Procesado. "
                    f"Opciones: {self.TIPOS_VALIDOS}"
                )

    return (Procesado,)


@app.cell
def _(ClassVar, Enum, List, Maquina, dataclass):
    class TipoCarguio(Enum):
        CARGADOR = "Cargador"
        GRUA = "Grúa"


    @dataclass(slots=False)
    class Carguio(Maquina):
        registro: ClassVar[
            List["Carguio"]
        ] = []  # para llevar la cuenta (se inicialia abajo)
        TIPOS_VALIDOS = {t.value for t in TipoCarguio}

        def __post_init__(self):
            super().__post_init__()
            Carguio.registro.append(self)
            if self.tipo_maquina not in self.TIPOS_VALIDOS:
                raise ValueError(
                    f"tipo_maquina '{self.tipo_maquina}' no válido para Carguio. "
                    f"Opciones: {self.TIPOS_VALIDOS}"
                )

    return (Carguio,)


@app.cell
def _(ClassVar, Enum, List, Maquina, dataclass):
    class TipoTransporte(Enum):
        CAMION = "Camion"


    @dataclass(slots=False)
    class Transporte(Maquina):
        registro: ClassVar[
            List["Transporte"]
        ] = []  # para llevar la cuenta (se inicialia abajo)
        TIPOS_VALIDOS = {t.value for t in TipoTransporte}

        def __post_init__(self):
            super().__post_init__()
            Transporte.registro.append(self)
            if self.tipo_maquina not in self.TIPOS_VALIDOS:
                raise ValueError(
                    f"tipo_maquina '{self.tipo_maquina}' no válido para Transporte Secundario. "
                    f"Opciones: {self.TIPOS_VALIDOS}"
                )

    return (Transporte,)


@app.cell
def _(mo):
    mo.md(r"""
    ## **INSTANCIAS (BASE DE DATOS)**
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Volteo
    """)
    return


@app.cell
def _(Volteo, pd):
    Volteo.registro.clear()
    VOLTEO_A = Volteo(
        nombre="Fellerbuncher 53.7",
        tipo_maquina="Fellerbuncher",
        productividad_maquina=75.64, # hrpr
        inversion_inicial=313_637_387,
        vida_util=4,
        disponibilidad=0.71,
        factor_reventa=0.2,
        factor_reparacion=0.8, # % decimal
        interes = 0.12, # % decimal
        impuestos = 0.175, # % decimal
        seguros = 0.02, # % decimal
        uso_anual_planificado = 3600,
        consumo_combustible=37,
        factor_lubricantes=0.067,
        sueldo_operador=1,
    )
    VOLTEO_B = Volteo(
        nombre="Fellerbuncher 3-1",
        tipo_maquina="Fellerbuncher",
        productividad_maquina=65.14,
        inversion_inicial=313_637_387,
        vida_util=4,
        disponibilidad=0.71,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=37,
        factor_lubricantes=0.067,
        sueldo_operador=1,
    )

    VOLTEO_C = Volteo(
        nombre="Fellerbuncher_PRI",
        tipo_maquina="Fellerbuncher",
        productividad_maquina=91.55,
        inversion_inicial=313_637_387,
        vida_util=4,
        disponibilidad=0.71,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=37,
        factor_lubricantes=0.067,
        sueldo_operador=1,
    )

    VOLTEO_D = Volteo(
        nombre="FB_53.7_2006",
        tipo_maquina="Fellerbuncher",
        productividad_maquina=75.64,
        inversion_inicial=300_000,
        vida_util=4,
        disponibilidad=0.71,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=37,
        factor_lubricantes=0.067,
        sueldo_operador=1)

    VOLTEO_E = Volteo(
        nombre="FB_53.7_2006_B",
        tipo_maquina="Fellerbuncher",
        productividad_maquina=74.56,
        inversion_inicial=300_000,
        vida_util=4,
        disponibilidad=0.72,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=37,
        factor_lubricantes=0.063,
        sueldo_operador=1)

    df_instancias_volteo = pd.DataFrame([
        {
            "Nombre": m.nombre,
            "Inversión ($)": m.inversion_inicial,
            "Prod. (m³/hr)": m.productividad_maquina,
            "Disponibilidad (%)": (m.disponibilidad*100),
            "CV ($/hrdi)": (round(m.cvm_hrdi, 2))
        }
        for m in Volteo.registro
    ])

    df_instancias_volteo
    return VOLTEO_A, VOLTEO_B, VOLTEO_C, VOLTEO_D


@app.cell
def _(VOLTEO_A, VOLTEO_B, VOLTEO_C, VOLTEO_D):
    VOLTEO_A.cvm_hrpr, VOLTEO_B.cvm_hrpr, VOLTEO_C.cvm_hrpr, (VOLTEO_D.cvm_hrpr)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Madereo
    """)
    return


@app.cell
def _(Madereo, pd):
    Madereo.registro.clear()
    MADEREO_A = Madereo(
        nombre="Skidder-Garra 53.7",
        tipo_maquina="Skidder-Garra",
        productividad_maquina=85.2,
        inversion_inicial=230_007_500,
        vida_util=4,
        disponibilidad=0.63,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=26,
        factor_lubricantes=0.065,
        sueldo_operador=1,
    )

    MADEREO_B = Madereo(
        nombre="Skidder-Garra 3-1",
        tipo_maquina="Skidder-Garra",
        productividad_maquina=53.97,
        inversion_inicial=230_007_500,
        vida_util=4,
        disponibilidad=0.63,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=26,
        factor_lubricantes=0.065,
        sueldo_operador=1,
    )

    MADEREO_C = Madereo(
        nombre="Skidder-Garra PRI",
        tipo_maquina="Skidder-Garra",
        productividad_maquina=63.49,
        inversion_inicial=230_007_500,
        vida_util=4,
        disponibilidad=0.63,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=26,
        factor_lubricantes=0.065,
        sueldo_operador=1,
    )

    MADEREO_D = Madereo(
        nombre="SG_53.7_2006",
        tipo_maquina="Skidder-Garra",
        productividad_maquina=85.2,
        inversion_inicial=220_000,
        vida_util=4,
        disponibilidad=0.63,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=26,
        factor_lubricantes=0.065,
        sueldo_operador=1,
    )



    df_instancias_madereo = pd.DataFrame([
        {
            "Nombre": m.nombre,
            "Tipo": m.tipo_maquina,
            "Inversión ($)": m.inversion_inicial,
            "Prod. (m³/hr)": m.productividad_maquina,
            "Disponibilidad (%)": (m.disponibilidad*100),
            "Vida útil (años)": m.vida_util,
        }
        for m in Madereo.registro
    ])

    df_instancias_madereo
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Procesado
    """)
    return


@app.cell
def _(Procesado, pd):
    Procesado.registro.clear()
    PROC_A = Procesado(
        nombre="Procesador 53.7",
        tipo_maquina="Procesador",
        productividad_maquina=34.87,
        inversion_inicial=250_909_909.44,
        vida_util=4,
        disponibilidad=0.77,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=27,
        factor_lubricantes=0.084,
        sueldo_operador=1,
    )

    PROC_B = Procesado(
        nombre="Procesador 3-1",
        tipo_maquina="Procesador",
        productividad_maquina=43.18,
        inversion_inicial=250_909_909.44,
        vida_util=4,
        disponibilidad=0.77,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=27,
        factor_lubricantes=0.084,
        sueldo_operador=1,
    )

    PROC_C = Procesado(
        nombre="Procesador PRI",
        tipo_maquina="Procesador",
        productividad_maquina=48.05,
        inversion_inicial=250_909_909.44,
        vida_util=4,
        disponibilidad=0.77,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=27,
        factor_lubricantes=0.084,
        sueldo_operador=1,
    )

    PROC_A = Procesado(
        nombre="PROC_53.7_2006",
        tipo_maquina="Procesador",
        productividad_maquina=34.87,
        inversion_inicial=240_000,
        vida_util=4,
        disponibilidad=0.77,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=27,
        factor_lubricantes=0.084,
        sueldo_operador=1,
    )

    df_instancias_procesado = pd.DataFrame([
        {
            "Nombre": m.nombre,
            "Tipo": m.tipo_maquina,
            "Inversión ($)": m.inversion_inicial,
            "Prod. (m³/hr)": m.productividad_maquina,
            "Disponibilidad (%)": (m.disponibilidad*100),
            "Vida útil (años)": m.vida_util,
        }
        for m in Procesado.registro
    ])

    df_instancias_procesado
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Carguio
    """)
    return


@app.cell
def _(Carguio, pd):
    Carguio.registro.clear()
    CARGUIO_A = Carguio(
        nombre="Grúa 53.7",
        tipo_maquina="Grúa",
        productividad_maquina=31.22,
        inversion_inicial=18_818_2432.08,
        vida_util=4,
        disponibilidad=0.86,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=18,
        factor_lubricantes=0.106,
        sueldo_operador=1,
    )

    CARGUIO_B = Carguio(
        nombre="Grúa 3-1",
        tipo_maquina="Grúa",
        productividad_maquina=30.52,
        inversion_inicial=18_818_2432.08,
        vida_util=4,
        disponibilidad=0.86,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=18,
        factor_lubricantes=0.106,
        sueldo_operador=1,
    )

    CARGUIO_C = Carguio(
        nombre="Grúa PRI",
        tipo_maquina="Grúa",
        productividad_maquina=34.88,
        inversion_inicial=18_818_2432.08,
        vida_util=4,
        disponibilidad=0.86,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=18,
        factor_lubricantes=0.106,
        sueldo_operador=1,
    )

    CARGUIO_D = Carguio(
        nombre="Grúa_53.7_2006",
        tipo_maquina="Grúa",
        productividad_maquina=31.22,
        inversion_inicial=180_000,
        vida_util=4,
        disponibilidad=0.86,
        factor_reventa=0.2,
        factor_reparacion=0.8,
        interes = 0.12, # decimal
        impuestos = 0.175, # decimal
        seguros = 0.02, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=18,
        factor_lubricantes=0.106,
        sueldo_operador=1,
    )

    df_instancias_carguio = pd.DataFrame([
        {
            "Nombre": m.nombre,
            "Tipo": m.tipo_maquina,
            "Inversión ($)": m.inversion_inicial,
            "Prod. (m³/hr)": m.productividad_maquina,
            "Disponibilidad (%)": (m.disponibilidad*100),
            "Vida útil (años)": m.vida_util,
        }
        for m in Carguio.registro
    ])

    df_instancias_carguio
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Transporte Secundario
    """)
    return


@app.cell
def _(PT, Transporte, pd):
    Transporte.registro.clear()
    TRANSPORTE_A = Transporte(
        nombre="Camión de Prueba",
        tipo_maquina="Camion",
        productividad_maquina= PT, # Donde PT es la productividad del camión
        inversion_inicial=0.0000000001,
        vida_util=100,
        disponibilidad=1,
        factor_reventa=1,
        factor_reparacion=0.0000001,
        interes = 0.001, # decimal
        impuestos = 0.0001, # decimal
        seguros = 0.00001, # decimal
        uso_anual_planificado = 3600,
        consumo_combustible=0.00000001,
        factor_lubricantes=0.000000000106,
        sueldo_operador=0.0000000001,
    )

    df_instancias_transporte = pd.DataFrame([
        {
            "Nombre": m.nombre,
            "Tipo": m.tipo_maquina,
            "Inversión ($)": m.inversion_inicial,
            "Prod. (m³/hr)": m.productividad_maquina,
            "Disponibilidad (%)": (m.disponibilidad*100),
            "Vida útil (años)": m.vida_util,
        }
        for m in Transporte.registro
    ])

    df_instancias_transporte
    return (TRANSPORTE_A,)


@app.cell
def _():

    b0 = 2
    m = 2
    tabla = [ b0+i*m for i in range(1,13)]

    tabla
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""
    <br><br>
    # 3 Análisis del sistema
    """)
    return


@app.cell
def _(Carguio, Madereo, Procesado, Transporte, Volteo, mo):
    # Volteo
    opciones_volteo = [v.nombre for v in Volteo.registro]
    dd_selector_volteo = mo.ui.dropdown(
        opciones_volteo, value=opciones_volteo[0] if opciones_volteo else None
    )
    dd_n_volteo = mo.ui.dropdown(range(1, 11), value=1)
    dd_operadores_volteo = mo.ui.dropdown(range(1, 11), value=2)

    # Madereo
    opciones_madereo = [m.nombre for m in Madereo.registro]
    dd_selector_madereo = mo.ui.dropdown(
        opciones_madereo, value=opciones_madereo[0] if opciones_madereo else None
    )
    dd_n_madereo = mo.ui.dropdown(range(1, 11), value=1)
    dd_operadores_madereo = mo.ui.dropdown(range(1, 11), value=2)

    # Procesado
    opciones_procesado = [p.nombre for p in Procesado.registro]
    dd_selector_procesado = mo.ui.dropdown(
        opciones_procesado,
        value=opciones_procesado[0] if opciones_procesado else None,
    )
    dd_n_procesado = mo.ui.dropdown(range(1, 11), value=2)
    dd_operadores_procesado = mo.ui.dropdown(range(1, 11), value=3)

    # Carguio
    opciones_carguio = [c.nombre for c in Carguio.registro]
    dd_selector_carguio = mo.ui.dropdown(
        opciones_carguio, value=opciones_carguio[0] if opciones_carguio else None
    )
    dd_n_carguio = mo.ui.dropdown(range(1, 11), value=2)
    dd_operadores_carguio = mo.ui.dropdown(range(1, 11), value=4)


    # Transporte
    opciones_transporte = [ts.nombre for ts in Transporte.registro]
    dd_selector_transporte = mo.ui.dropdown(
        opciones_transporte,
        value=opciones_transporte[0] if opciones_transporte else None,
    )
    dd_n_transporte = mo.ui.dropdown(range(1, 11), value=1)
    dd_operadores_transporte = mo.ui.dropdown(range(1, 11), value=1)
    return (
        dd_n_carguio,
        dd_n_madereo,
        dd_n_procesado,
        dd_n_transporte,
        dd_n_volteo,
        dd_operadores_carguio,
        dd_operadores_madereo,
        dd_operadores_procesado,
        dd_operadores_transporte,
        dd_operadores_volteo,
        dd_selector_carguio,
        dd_selector_madereo,
        dd_selector_procesado,
        dd_selector_transporte,
        dd_selector_volteo,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## Funciones
    """)
    return


@app.cell(hide_code=True)
def _(i, mo):
    mo.md(rf"""
    ### Productividad Subsistemas
    La *productividad de los subsistemas* es la razón entre la producción respecto del tiempo requerido para conseguirla. La unidad más común para expresarla es el volumen respecto del tiempo $(m^3/hr)$. El tiempo se puede clasificar en 3 categorías: *tiempo planificado*, correspondiente a la jornada laboral establecida para una máquina o subsitema; *tiempo disponible* que es el tiempo en que una máquina está en condiciones de ejecutar trabajos (es decir descontando el tiempo de mantención y carga de combustible); *tiempo productivo*, que es el tiempo en que una máquina esta efectivamente realizando el trabajo para el cual fué diseñado. La disponibilidad a nivel de subsistema se calcula considerando la productividad individual de cada máquina, su disponibilidad mecánica y la cantidad de la máquina seleccionada, de la siguiente manera:
    - Sean:
      - $PMhrpr_{i} =$ Productividad individual de la máquina seleccionada en el subsistema $i$, en horas **productivas** $(m^3/hrpr)$.
      - $DM_i =$ Disponibilidad mecánica de la máquina seleccionada en el subsistema $i$ $(\%)$.
      - $PMhrdi_i$ = Productividad individual de la máquina seleccionada en el subsistema $i$, en horas **disponibles** $(m^3/hrdi)$, donde:
       - \[PMhrdi_i = PMhrpr_i \cdot DM_i\]
      - $N_i =$ Cantidad de la máquina seleccionada en el subsistema $i$ $(cantidad)$.
      - $PSShrdi_i$ = Productividad del subsistema $i$, en horas **disponibles** $(m^3/hrdi)$, donde:
        - \[PSS_i = PMhrdi_i \cdot N_i\]
    """)
    return


@app.cell
def _(
    carguio_sel,
    dd_n_carguio,
    dd_n_madereo,
    dd_n_procesado,
    dd_n_transporte,
    dd_n_volteo,
    madereo_sel,
    procesado_sel,
    transporte_sel,
    volteo_sel,
):
    def productividad_ss(subsistema:str):
        "Calcula la productividad en base a las horas disponibles(m^3/hrdi) de un determinado subsistema, el cual debe ser pasado como argumento"

        subsistema = subsistema.capitalize()

        subsistemas_posibles = ["Volteo", "Madereo", "Procesado", "Carguio", "Transporte"]

        if subsistema == "Volteo":
            return (volteo_sel.productividad_maquina*
                    volteo_sel.disponibilidad*
                    dd_n_volteo.value)
        elif subsistema == "Madereo":
            return (madereo_sel.productividad_maquina*madereo_sel.disponibilidad*dd_n_madereo.value)
        elif subsistema == "Procesado":
            return (procesado_sel.productividad_maquina*procesado_sel.disponibilidad*dd_n_procesado.value)
        elif subsistema == "Carguio":
            return (carguio_sel.productividad_maquina*carguio_sel.disponibilidad*dd_n_carguio.value)
        elif subsistema == "Transporte":
            return (transporte_sel.productividad_maquina*transporte_sel.disponibilidad*dd_n_transporte.value)
        else:
            return ValueError(f"Subsistema inválido. Los subsistemas posibles son : {subsistemas_posibles}")

    return (productividad_ss,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Cuello de Botella <br>
    El cuello de botella es el menor valor entre la productividad  disponible de cada subsistema y la capacidad de recepción en planta. Este valor representa también la productividad potencial ya que causar pérdida de productividad en los subsistemas con mayor productividad disponible debido a la falta de producción. La forma para calcularla es la siguiente:
    - Sean:
      - $PSS_{1}, PSS_{2}... PSS_{n} =$ Productividad de los Subsistemas $(m^3/hrdi)$.
      - $R =$ Capacidad de recepción en planta $(m^3/hrdi)$.
      - $CB =$ Cuello de botella $(m^3hrdi^{-1})$.
        - \[CB = menor(PSS_{1}, PSS_{2}... PSS_{n}, R)\]
    """)
    return


@app.cell
def _(namedtuple, productividad_ss, recepcion_planta_m3hrpl):
    CuelloBotella = namedtuple("CuelloBotella", ["causa", "valor"])

    def cuello_botella():
        opciones = {"Volteo": productividad_ss("Volteo"),
                    "Madereo": productividad_ss("Madereo"),
                    "Procesado": productividad_ss("Procesado"),
                    "Carguio": productividad_ss("Carguio"),
                    "Transporte": productividad_ss("Transporte"),
                    "RecepcionPlanta": recepcion_planta_m3hrpl}

        causa = min(opciones, key=opciones.get)
        return CuelloBotella(causa, opciones[causa])

    cuello_botella = cuello_botella()  # para poder llamar a la causa o valor con el formato cuello_botella.valor, sin necesidad de ser cuello_botella().valor. Lo mismo para cuello_botella.causa
    return (cuello_botella,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Utilización de los subsistemas<br>
    La *utilización* es la razón entre del uso efectivo para la cantidad y tipo de máquinas definidas en en cada subsistema (horas productivas), respecto del uso potencial (horas planificadas). En este contexto, la forma para calcular la utilización es distinta para los subsistemas productivos (*Volteo, Madereo, procesado, Carguío*) resepcto del subsistema *Transporte*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Subsistemas Productivos
    Para los subsistemas productivos, la utilización se calcula como el porcentaje que representa el cuello de botella respecto de la productividad del subsistema en horas disponibles de las máquinas, de la siguiente manera: <br>
    - Sean:
      - $i$ cada uno de los subsistemas productivos $(Volteo, Madereo, Procesado, Carguío)$.
      - $PMhrpr_i$ la productividad individual de la máquina selecionada en el subsistema $i$, en horas **productivas** $(m^3hrpr^{-1})$.
      - $DM_i$ la disponibilidad mecánica de la máquina seleccionada en el susbsistema $i$ $(\%)$.
      - $N_i$ la cantidad de  máquinas asignadas en el subsistema $i$ $(cantidad)$.
      - $CB$ el cuello de botella del sistema de cosecha configurado $(m^3hrdi^{-1})$.
      - $PSShrdi_i$ es la productividad del subsistema $i$ $(\$^1hrdi^{-1})$, donde:
       - \[PSShrdi_i = PMhrpr_i \cdot DM_i \cdot N_i \]
      - $U_{i}$ La utilización del subsistema $i$ $(\%)$, donde:
        - \[ U_i = \frac{CB}{PSShrdi_i}\]
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Subsistema Transporte
    El subsistema de *Transporte* tiene una planificación horaria independiente a los otros subsistemas, el cual se define en el submódulo *1.3 Transporte  Secundario* los cuales tienen una jornada laboral en común que se define en el súbmódulo *1.2 Programación del Trabajo*. Es por esta razón que para el subsistema transporte, la *Utilización* recibe un factor de corrección horaria, equivalente a la razón entre la jornada laboral diaria del los subsistemas productivos *(HD)* resepcto de la jornada laboral diaria del transporte *HDT*. La utilización es el menor valor entre la disponibilidad mecánica de la máquina seleccionada en el subsistema transporte y la utilización corregida, mencionada anteriormente. La utilización del subsistema transporte se calcula de la siguiente manera:<br>

    - Sean:
      - $PMhrpr_t$ $(m^3hrpr^{-1}):$ productividad individual de la máquina seleccionada en el subsistema de *Transporte*, en horas **productivas**.
      - $DM_t$ $(\%):$ disponibilidad mecánica de la máquina seleccionada en el subsistema *Transporte*.
      - $N_t$ $(cantidad):$ cantidad de de la máquina seleccionada en el subsistema *Transporte*.
      - $CB$ $(m^3hrdi^{-1}):$ cuello de botella del sistema de cosecha.
      - $PSShrdi_t$ la productividad del subsistema de transporte  $(m^3hrdi^{-1})$, donde:
        - \[PSShrdi_t = PMhrpr_t \cdot DM_t \cdot N_t \]
      - $HD$ $(horas^1día^{-1}):$ jornada laboral planificada para los subsistemas *Productivos*.
      - $HDT$ $(horas^1día^{-1}):$ jornada laboral planificada para el subsistema *Transporte*.
      - $U_t$ ,donde:
        - \[U_t = menor(DM_t, \frac{CB}{PSShrdi_t}*\frac{HD}{HDT})\]
    """)
    return


@app.cell
def _(HD, HDT, cuello_botella, productividad_ss, transporte_sel):

    def utilizacion_ss(subsistema)-> float:
        if subsistema == "Volteo":
            return (cuello_botella.valor/ productividad_ss("Volteo"))
        elif subsistema == "Madereo":
            return (cuello_botella.valor/ productividad_ss("Madereo") )
        elif subsistema == "Procesado":
            return (cuello_botella.valor/ productividad_ss("Procesado"))
        elif subsistema == "Carguio":
            return (cuello_botella.valor/ productividad_ss("Carguio"))
        elif subsistema == "Transporte":
            return min(transporte_sel.disponibilidad, (cuello_botella.valor/transporte_sel.productividad_maquina*HD/HDT))
        else:
            return "subsistemas posibles son Volteo, Madereo, Procesado, Carguio, Transporte"

    utilizacion_ss("Transporte")
    return (utilizacion_ss,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Costos por Subsistema
    Los costos por subsistema considera los costos *fijos* y *variables* utilizando el método tarifa de máquina *(Brinker et al 2002)*, con la diferencia que los costo de *mano de obra* se calculan de forma independiente a los *costos variables*. El cálculo a nivel de máquina proviene de la base de datos de las máquinas creadas (instancias).

    ### Costos Fijos (CF)
    Los costos fijos son aquellos en que se incurre independientemente de la producción, por lo se suelen expresar en función de las horas planificadas que comprenden el total del horario laboral $(\$^1hrpl^{-1})$, de la siguiente forma:
    - Sean:
      - $CFMhrpl_i$ el costo fijo de una unidad de la máquina seleccionada en el subsistema $i$ $(\$^1hrpl^{-1})$.
      - $N_i$ el número de máquinas asignadas en el subsistema $i$ $(cantidad)$.
      - $CFSShrpl_i$ Los costos fijos del subsistema $i$ $(\$^1hrpl^{-1})$, donde:
        - \[CFSShrpl_i = CFMhrpl_i \cdot N_i\]

    ### Costos Variables (CV)
    Los costos variables son aquellos que están directamente relacionados con la productividad de las máquinas, por lo que están afectados tanto por la disponibilidad mecánica$(\%)$ como por la utilización$(\%)$ de las máquinas. El cálculo se realiza de la siguiente forma:
    - Sean:
      - $CVMhrpr_i(\$hrpr^{-1})$ el costo fijo de una unidad de la máquina seleccionada en el subsistema $i$, en **horas productivas**.
      - $CVSShrpl_i(\$hrpl^{-1})$ el costo variable del subsistema $i$ en **horas planificadas**, donde:
        - \[CVSShrpl_i = CVhrpr_i \cdot DM_i \cdot N_i \cdot U_i \]

    ### Costos Manos de Obra (CMO)
    - Sean:
      - $SO (\$^1mes^{-1})$ Es el sueldo líquido del operador de la máquina seleccionada en el subsistema $i$.
      - $BS_i (\%)$ Es el porcentaje legal del sueldo destinado a los beneficios sociales.
      - $hrplmes_i (horas)$ Son las horas planificadas al mes para el operario del subsitema $i$.
      - $NMO_i (cantidad)$ Cantidad de operadores asignados por máquina para el subsistema $i$.
      - $CMOM_i (\$^1hr^{-1})$ Es el costo por hora del sueldo líquido de 1 operario de máquina del subsistema $i$, donde:
        - \[CMOM_i = (\frac{SO\cdot (1+BS_i)}{hrplmes_i}) \]
      - $CMOSS_i (\$^1hr^{-1})$ Costo de mano de obra por hora para el subsistema $i$, donde:
        - \[CMOSS_i = CMOM_i \cdot NMO_i \]
    """)
    return


@app.cell
def _(
    carguio_sel,
    dd_n_carguio,
    dd_n_madereo,
    dd_n_procesado,
    dd_n_transporte,
    dd_n_volteo,
    madereo_sel,
    procesado_sel,
    transporte_sel,
    volteo_sel,
):
    subsistemas_posibles = ["Volteo", "Madereo", "Procesado", "Carguio", "Transporte"]
    def cf_subsistema_hrpl(subsistema:str):

        if subsistema == "Volteo":
            return (volteo_sel.cfm_hrpl*dd_n_volteo.value)
        elif subsistema == "Madereo":
            return (madereo_sel.cfm_hrpl*dd_n_madereo.value)
        elif subsistema == "Procesado":
            return (procesado_sel.cfm_hrpl*dd_n_procesado.value)
        elif subsistema == "Carguio":
            return (carguio_sel.cfm_hrpl*dd_n_carguio.value)
        elif subsistema == "Transporte":
            return (transporte_sel.cfm_hrpl*dd_n_transporte.value)
        else:
            return ValueError(f"Subsistema inválido. Los subsistemas posibles son : {subsistemas_posibles}")

    cf_subsistema_hrpl("Volteo"), (cf_subsistema_hrpl("Madereo"))
    return cf_subsistema_hrpl, subsistemas_posibles


@app.cell
def _(
    carguio_sel,
    cf_subsistema_hrpl,
    cv_subsistema_hrdi,
    dd_n_carguio,
    dd_n_madereo,
    dd_n_procesado,
    dd_n_transporte,
    dd_n_volteo,
    dd_operadores_carguio,
    dd_operadores_madereo,
    dd_operadores_procesado,
    dd_operadores_transporte,
    dd_operadores_volteo,
    madereo_sel,
    procesado_sel,
    subsistemas_posibles,
    transporte_sel,
    utilizacion_ss,
    volteo_sel,
):
    def cv_subsistema_hrpl(subsistema: str):

        if subsistema == "Volteo":
            return (volteo_sel.cvm_hrdi *
                    dd_n_volteo.value *
                    utilizacion_ss("Volteo"))

        elif subsistema == "Madereo":
            return (madereo_sel.cvm_hrpr *
                    madereo_sel.disponibilidad*
                    dd_n_madereo.value *
                    utilizacion_ss("Madereo"))

        elif subsistema == "Procesado":
            return (procesado_sel.cvm_hrpr *
                    procesado_sel.disponibilidad*
                    dd_n_procesado.value *
                    utilizacion_ss("Procesado"))

        elif subsistema == "Carguio":
            return (carguio_sel.cvm_hrpr *
                    carguio_sel.disponibilidad*
                    dd_n_carguio.value *                
                    utilizacion_ss("Carguio"))

        elif subsistema == "Transporte":
            return (transporte_sel.cvm_hrpr*
                    transporte_sel.disponibilidad*
                    dd_n_transporte.value *
                    utilizacion_ss("Transporte"))

        else:
            raise ValueError(
                f"Subsistema inválido. Los subsistemas posibles son: {subsistemas_posibles}"
            )

    def cvt_sistema_hrpl() -> float:
        "Costos Variables totales"
        return sum(cv_subsistema_hrdi(ss) for ss in subsistemas_posibles)



    def cv_subsistema_hr_pr_pl(subsistema:str)->float:


        if subsistema == "Volteo":
            return (volteo_sel.cvm_hrpr*
                    volteo_sel.disponibilidad*
                    dd_n_volteo.value*
                    utilizacion_ss("Volteo"))
        elif subsistema == "Madereo":
            return (madereo_sel.cvm_hrpr*
                    madereo_sel.disponibilidad*
                    dd_n_madereo.value*
                    utilizacion_ss("Madereo"))
        elif subsistema == "Procesado":
            return (procesado_sel.cvm_hrpr*
                    procesado_sel.disponibilidad*
                    dd_n_procesado.value*
                    utilizacion_ss("Procesado"))
        elif subsistema == "Carguio":
            return (carguio_sel.cvm_hrpr*
                    carguio_sel.disponibilidad*
                    dd_n_carguio.value
                    *utilizacion_ss("Carguio"))
        elif subsistema == "Transporte":
            return (transporte_sel.cvm_hrpr*
                    transporte_sel.disponibilidad*
                    dd_n_transporte.value*
                    utilizacion_ss("Transporte"))
        else:
            raise ValueError(
                f"Subsistema inválido. Los subsistemas posibles son: {subsistemas_posibles}"
            )

    def cmo_subsistema_hrpl(subsistema:str)->float :

        if subsistema == "Volteo":
            return (volteo_sel.cmom_hrpl*dd_operadores_volteo.value)
        elif subsistema == "Madereo":
            return (madereo_sel.cmom_hrpl*dd_operadores_madereo.value)
        elif subsistema == "Procesado":
            return (procesado_sel.cmom_hrpl*dd_operadores_procesado.value)
        elif subsistema == "Carguio":
            return (carguio_sel.cmom_hrpl * dd_operadores_carguio.value)
        elif subsistema == "Transporte":
            return (transporte_sel.cmom_hrpl*dd_operadores_transporte.value)
        else:
            raise ValueError(
                f"Subsistema inválido. Los subsistemas posibles son: {subsistemas_posibles}"
            )

    def cft_sistema(subsistemas)->float:
        """ Costo Fijo Total del Sistema($/hrpl)"""
        return sum(cf_subsistema_hrpl(s) for s in subsistemas)

    def cvt_sistema(subsistemas)->float:
        """ Costo Variable Total del Sistema($/hrpl)"""
        return sum(cv_subsistema_hrpl(s) for s in subsistemas)

    def cvt_sistema_hrpr_pl(subsistemas)->float:
        """ Costo Variable Total del Sistema($/hrpl)"""
        return sum(cv_subsistema_hr_pr_pl(s) for s in subsistemas)

    def cmot_sistema(subsistemas)->float:
        """ Costo Mano de Obra Total del Sistema($/hrpl)"""
        return sum(cmo_subsistema_hrpl(s) for s in subsistemas)

    return (
        cft_sistema,
        cmo_subsistema_hrpl,
        cmot_sistema,
        cv_subsistema_hr_pr_pl,
        cv_subsistema_hrpl,
        cvt_sistema,
        cvt_sistema_hrpr_pl,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## Panel Selección de Máquinas
    """)
    return


@app.cell
def _(
    dd_n_carguio,
    dd_n_madereo,
    dd_n_procesado,
    dd_n_transporte,
    dd_n_volteo,
    dd_operadores_carguio,
    dd_operadores_madereo,
    dd_operadores_procesado,
    dd_operadores_transporte,
    dd_operadores_volteo,
    dd_selector_carguio,
    dd_selector_madereo,
    dd_selector_procesado,
    dd_selector_transporte,
    dd_selector_volteo,
    mo,
):
    panel1 = mo.vstack(
        [
            mo.md("**Configuración Sistema de cosecha**"),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("<br>"),
                            mo.md("*Máquina :*"),
                            mo.md("*Cantidad :*"),
                            mo.md("*n Operadores :*")],align="center"
                    ),
                    mo.vstack(
                        [
                            mo.md("**Volteo**"),
                            dd_selector_volteo,
                            dd_n_volteo,
                            dd_operadores_volteo,
                            ],
                        align="center",
                    ),
                    mo.vstack(
                        [
                            mo.md("**Madereo**"),
                            dd_selector_madereo,
                            dd_n_madereo,
                            dd_operadores_madereo
                        ],
                        align="center",
                    ),
                    mo.vstack(
                        [
                            mo.md("**Procesado**"),
                            dd_selector_procesado,
                            dd_n_procesado,
                            dd_operadores_procesado,
                        ],
                        align="center",
                    ),
                    mo.vstack(
                        [
                            mo.md("**Carguío**"),
                            dd_selector_carguio,
                            dd_n_carguio,
                            dd_operadores_carguio,
                        ],
                        align="center",
                    ),
                    mo.vstack(
                        [
                            mo.md("**Transporte**"),
                            dd_selector_transporte,
                            dd_n_transporte,
                            dd_operadores_transporte,
                        ],
                        align="center",
                    ),
                ]
            ),
        ]
    )
    return (panel1,)


@app.cell
def _(
    Carguio,
    Madereo,
    Procesado,
    Transporte,
    Volteo,
    dd_selector_carguio,
    dd_selector_madereo,
    dd_selector_procesado,
    dd_selector_transporte,
    dd_selector_volteo,
):
    volteo_sel = next(
        v for v in Volteo.registro if v.nombre == dd_selector_volteo.value
    )
    madereo_sel = next(
        m for m in Madereo.registro if m.nombre == dd_selector_madereo.value
    )
    procesado_sel = next(
        p for p in Procesado.registro if p.nombre == dd_selector_procesado.value
    )
    carguio_sel = next(
        c for c in Carguio.registro if c.nombre == dd_selector_carguio.value
    )
    transporte_sel = next(
        t for t in Transporte.registro if t.nombre == dd_selector_transporte.value
    )
    return carguio_sel, madereo_sel, procesado_sel, transporte_sel, volteo_sel


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## SIMULACIÓN SISTEMA DE COSECHA
    """)
    return


@app.cell
def _(panel1):
    panel1
    return


@app.cell
def _(df_resultados, mo):
    mo.vstack([mo.md("### Reporte :"), df_resultados])
    return


@app.cell
def _(
    cf_subsistema_hrpl,
    cft_sistema,
    cmo_subsistema_hrpl,
    cmot_sistema,
    cuello_botella,
    cv_subsistema_hr_pr_pl,
    cv_subsistema_hrpl,
    cvt_sistema,
    cvt_sistema_hrpr_pl,
    pd,
    productividad_ss,
    subsistemas_posibles,
    utilizacion_ss,
):
    dicc_resultados = {
        "Item": [
            "Productividad (m³/hrpl)",
            "Utilización (%)",
            "Costos Fijos ($/hrpl)",
            "Costos Variables ($/hrpl)",
            "Costos Variables pr ($/hr_pr_pl)",
            "Costos Mano de Obra ($/hrpl)",
            "Total ($/hrpl)"
        ]
    }

    columna_sistema = {
        "Sistema": [
            round(cuello_botella.valor, 1),
            pd.NA,
            round(cft_sistema(subsistemas_posibles)),
            round(cvt_sistema(subsistemas_posibles)),
            round(cvt_sistema_hrpr_pl(subsistemas_posibles)),
            round(cmot_sistema(subsistemas_posibles)),
            round(
                cft_sistema(subsistemas_posibles)
                + cvt_sistema(subsistemas_posibles)
                + cmot_sistema(subsistemas_posibles)
            )
        ]
    }

    for i in subsistemas_posibles:
        dicc_resultados[i] = [
            round(productividad_ss(i), 1),
            round(utilizacion_ss(i) * 100),
            round(cf_subsistema_hrpl(i), 2),
            round(cv_subsistema_hrpl(i), 2),
            round(cv_subsistema_hr_pr_pl(i), 2),
            round(cmo_subsistema_hrpl(i), 2),
            round((cf_subsistema_hrpl(i)
                  + cv_subsistema_hrpl(i)
                  + cmo_subsistema_hrpl(i)), 2)
        ]

    dicc_resultados.update(columna_sistema)

    df_resultados = pd.DataFrame(dicc_resultados)
    return df_resultados, i


@app.cell
def _(HD, VTC, cuello_botella):
    productividad_diaria_sistema = int(cuello_botella.valor*HD) # rendimiento menot * horas siarias laborales
    jornadas_cosecha = (VTC/productividad_diaria_sistema)
    return (jornadas_cosecha,)


@app.cell
def _(VTC, cuello_botella, jornadas_cosecha, mo):
    mo.md(rf"""
    ##CONCLUSIÓN
    &nbsp;&nbsp;&nbsp;La productividad del sistema es de ${cuello_botella.valor:.1f}$ $m^{3}/hrpl$. La causa del cuello de botella en la cadena productiva es el ${cuello_botella.causa}$. A este ritmo de producción, se estima que los {VTC:.1f} $m^3$ calculados para esta faena serán cosechados en **${int(jornadas_cosecha)}$** jornadas laborales<br>
    """)
    return


if __name__ == "__main__":
    app.run()

# coding: utf-8
from sqlalchemy import (
    CHAR, Column, DECIMAL, Date, Float, ForeignKey, ForeignKeyConstraint, Index,
    Integer, SmallInteger, String, Table, text
)
from sqlalchemy.dialects.mysql import CHAR, DECIMAL, INTEGER, MEDIUMINT, SET, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Abuelos(Base):
    __tablename__ = 'Abuelos'

    idAbuelo = Column(MEDIUMINT, primary_key=True)
    abuelo = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    corridas = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    ganadas = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    clasicos = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    places = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    terceros = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cuartos = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    quintos = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))

    # Relación con Madres
    madres = relationship("Madres", back_populates="abuelo")


class Madres(Base):
    __tablename__ = 'Madres'

    idMadre = Column(MEDIUMINT, primary_key=True)
    madre = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    idAbuelo = Column(MEDIUMINT, ForeignKey('Abuelos.idAbuelo', ondelete='RESTRICT', onupdate='CASCADE'),
                      nullable=False, server_default=text("'5534'"))

    abuelo = relationship("Abuelos", back_populates="madres")
    caballos = relationship("Caballos", back_populates="madre")


class Apuestas(Base):
    __tablename__ = 'Apuestas'

    idApuesta = Column(TINYINT, primary_key=True, unique=True)
    nombre = Column(CHAR(15), nullable=False, server_default=text("''"))
    carreras = Column(TINYINT, nullable=False, server_default=text("'1'"))


class Catedras(Base):
    __tablename__ = 'Catedras'
    __table_args__ = (
        Index('fk_ReuCab_Cat_idx', 'idHipodromo', 'fecha', 'referencia'),
    )

    idHipodromo = Column(TINYINT, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False, server_default=text("'1952-11-19'"))
    referencia = Column(SMALLINT, primary_key=True, nullable=False, server_default=text("'1'"))
    idMedio = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'1'"))
    pronostico = Column(TINYINT, server_default=text("'0'"))
    puntos = Column(SMALLINT, server_default=text("'0'"))


class Clasicos(Base):
    __tablename__ = 'Clasicos'

    idClasico = Column(SMALLINT, primary_key=True)
    idHipodromo = Column(TINYINT, nullable=False, server_default=text("'0'"))
    generico = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    nombre = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    sinComillas = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    marcador = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    grupo = Column(VARCHAR(3), nullable=False, server_default=text("''"))

    # Relación con ReunionCarreras sin crear FK física
    reunion_carreras = relationship("ReunionCarreras", 
                                   back_populates="clasico",
                                   primaryjoin="Clasicos.idClasico == ReunionCarreras.idClasico",
                                   foreign_keys="ReunionCarreras.idClasico")

class Colores(Base):
    __tablename__ = 'Colores'

    idColor = Column(TINYINT, primary_key=True)
    color = Column(VARCHAR(16), server_default=text("''"))
    breve = Column(VARCHAR(12), server_default=text("''"))
    código = Column(CHAR(3), server_default=text("''"))
    colorHembra = Column(VARCHAR(16), server_default=text("''"))

    caballos = relationship("Caballos", back_populates="color")


class Comentarios(Base):
    __tablename__ = 'Comentarios'

    idHipodromo = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, primary_key=True, nullable=False)
    referencia = Column(SMALLINT, primary_key=True, nullable=False)
    idCaballo = Column(MEDIUMINT, primary_key=True, nullable=False)
    realCajon = Column(TINYINT, nullable=False)
    cajon = Column(CHAR(4), nullable=False)
    votos = Column(TINYINT, nullable=False, server_default=text("'0'"))
    EstudiePata = Column(CHAR(3), nullable=False, server_default=text("''"))
    estudieComentario = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    startPata = Column(VARCHAR(2), nullable=False, server_default=text("''"))
    startComentario = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    burreroPata = Column(VARCHAR(2), nullable=False, server_default=text("''"))
    burreroComentario = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    datoPata = Column(VARCHAR(2), nullable=False, server_default=text("''"))
    datoCabeza = Column(CHAR(1), nullable=False, server_default=text("''"))
    datoComentario = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    apronte = Column(VARCHAR(2), nullable=False, server_default=text("''"))
    líneaTiempo = Column(CHAR(5), nullable=False, server_default=text("''"))
    pataLinea = Column(VARCHAR(2), nullable=False, server_default=text("''"))
    __table_args__ = (
        ForeignKeyConstraint(
            ['idHipodromo', 'fecha', 'referencia', 'idCaballo'],
            ['ReunionCaballos.idHipodromo', 'ReunionCaballos.fecha', 'ReunionCaballos.referencia', 'ReunionCaballos.idCaballo'],
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
    )
    reunion_caballo = relationship("ReunionCaballos", back_populates="comentarios")

    
class Condiciones(Base):
    __tablename__ = 'Condiciones'

    idCondicion = Column(SMALLINT, primary_key=True)
    idHipodromo = Column(TINYINT, nullable=False)
    condicion = Column(VARCHAR(100), nullable=False, server_default=text("''"))
    resultados = Column(VARCHAR(100), nullable=False, server_default=text("''"))
    startRefe = Column(CHAR(3), nullable=False, server_default=text("''"))
    condicionDato = Column(VARCHAR(30), nullable=False, server_default=text("''"))
    jcp = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    verdadera = Column(VARCHAR(25), nullable=False, server_default=text("''"))


class CondicionesEstudie(Base):
    __tablename__ = 'CondicionesEstudie'

    idCondicion = Column(SMALLINT, primary_key=True)
    codigo = Column(VARCHAR(14), nullable=False, server_default=text("''"))
    jcp = Column(VARCHAR(255), server_default=text("''"))
    condicion = Column(VARCHAR(255), server_default=text("''"))
    idCond = Column(SMALLINT, nullable=False)


class CondicionesNuevas(Base):
    __tablename__ = 'CondicionesNuevas'

    idCondicion = Column(INTEGER, primary_key=True)
    jcpSimple = Column(VARCHAR(256), nullable=False, server_default=text("''"))
    jcp = Column(VARCHAR(256), nullable=False, server_default=text("''"))
    condicion = Column(VARCHAR(256), nullable=False, server_default=text("''"))
    idCondicionSimple = Column(Integer, nullable=False, server_default=text("'0'"))
    condicionSimple = Column(VARCHAR(256), nullable=False, server_default=text("''"))
    resultados = Column(VARCHAR(40), nullable=False, server_default=text("''"))
    startRef = Column(VARCHAR(4), nullable=False, server_default=text("''"))
    dato = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    clase = Column(VARCHAR(6), nullable=False, server_default=text("''"))
    estudieRef = Column(VARCHAR(30), nullable=False, server_default=text("''"))
    tipo = Column(VARCHAR(6), nullable=False, server_default=text("''"))
    edad = Column(VARCHAR(5), nullable=False, server_default=text("''"))
    gMin = Column(Integer, nullable=False, server_default=text("'0'"))
    gMax = Column(Integer, nullable=False, server_default=text("'0'"))

    # Relación con ReunionCarreras
    reunion_carreras = relationship("ReunionCarreras", back_populates="condicion_nueva")


class Contratiempos(Base):
    __tablename__ = 'Contratiempos'

    idContratiempo = Column(INTEGER, primary_key=True)
    codigo = Column(VARCHAR(10), nullable=False, server_default=text("''"))
    contratiempo = Column(VARCHAR(200), nullable=False, server_default=text("''"))
    generico = Column(VARCHAR(3), nullable=False, server_default=text("''"))

    # Many-to-many con ReunionCaballos a través de ReunionContratiempos
    reuniones_caballos = relationship("ReunionCaballos", secondary="ReunionContratiempos", back_populates="contratiempos")


class Correcciones(Base):
    __tablename__ = 'Correcciones'

    id = Column(Integer, primary_key=True)
    tabla = Column(VARCHAR(25), nullable=False)
    dice = Column(VARCHAR(250), nullable=False)
    debe_decir = Column(VARCHAR(250), nullable=False)


class Criadores(Base):
    __tablename__ = 'Criadores'

    idCriador = Column(MEDIUMINT, primary_key=True, unique=True)
    criador = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    pais = Column(VARCHAR(4), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    clasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))

    # Relación con Caballos
    caballos = relationship("Caballos", back_populates="criador")

"""
class ErroresComunes(Base):
    __tablename__ = 'ErroresComunes'

    texto_original = Column(VARCHAR(180), primary_key=True)
    texto_corregido = Column(VARCHAR(180), nullable=False)
"""

class ErroresComunes(Base):
    __tablename__ = 'ErroresComunes'
    
    texto_original = Column(String(180, collation="utf8mb4_unicode_ci"), primary_key=True, nullable=False)
    texto_corregido = Column(String(180, collation="utf8mb4_unicode_ci"), nullable=False)

class Estilos(Base):
    __tablename__ = 'Estilos'

    idEstilo = Column(String(100), primary_key=True, server_default=text("''"))
    nombreQuark = Column(String(255), nullable=False, server_default=text("''"))
    nombreIDS = Column(String(255), nullable=False, server_default=text("''"))
    quarkDef = Column(String(255), nullable=False, server_default=text("''"))
    idsDef = Column(String(255), nullable=False, server_default=text("''"))


class HistoriaReunion(Base):
    __tablename__ = 'HistoriaReunion'

    nombre = Column(VARCHAR(25), primary_key=True, nullable=False, server_default=text("''"))
    rFecha = Column(Date, primary_key=True, nullable=False)
    rReferencia = Column(SMALLINT, primary_key=True, nullable=False)
    cajon = Column(TINYINT, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, nullable=False)
    referencia = Column(SMALLINT, nullable=False)
    idCaballo = Column(MEDIUMINT, nullable=False)
    kilos = Column(SMALLINT, server_default=text("'0'"))
    idJinete = Column(MEDIUMINT, server_default=text("'0'"))
    idPreparador = Column(MEDIUMINT, server_default=text("'0'"))
    jinete = Column(VARCHAR(20), server_default=text("''"))
    preparador = Column(VARCHAR(25))
    realCajon = Column(TINYINT, server_default=text("'0'"))
    pista = Column(SET('A', 'C', 'N'), server_default=text("'A'"))
    distancia = Column(SMALLINT, server_default=text("'0'"))
    baranda = Column(TINYINT, server_default=text("'0'"))
    tiempo = Column(String(10))
    corrieron = Column(TINYINT, server_default=text("'0'"))
    puesto = Column(TINYINT, server_default=text("'0'"))
    empate = Column(TINYINT, server_default=text("'0'"))
    favorito = Column(TINYINT, server_default=text("'0'"))
    soles = Column(DECIMAL(7, 2))
    separacion = Column(VARCHAR(17), server_default=text("''"))
    handicap = Column(VARCHAR(4), server_default=text("''"))
    pesoFisico = Column(SmallInteger, server_default=text("'0'"))
    desarrollo = Column(VARCHAR(6), server_default=text("''"))
    verdadera = Column(VARCHAR(25))
    ganador = Column(String(30))
    segundo = Column(String(30))
    tercero = Column(String(30))
    cuarto = Column(String(30))
    quinto = Column(String(30))
    sexto = Column(String(30))


class Jinetes(Base):
    __tablename__ = 'Jinetes'

    idJinete = Column(MEDIUMINT, primary_key=True)
    start = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    resultados = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    jcp = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    jinete = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(18), nullable=False, server_default=text("''"))
    estudie = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    aprendiz = Column(TINYINT, nullable=False, server_default=text("'0'"))
    apellido = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    nombre = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    brevisimo = Column(VARCHAR(12), nullable=False, server_default=text("''"))
    completo = Column(VARCHAR(30), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    quintos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    noPremio = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    ultimo = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    favorito = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasFavorito = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasClasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasClasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sinGanar = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    activo = Column(TINYINT, nullable=False, server_default=text("'0'"))
    ordenEstadistica = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corrUltSem = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganUltSem = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    totalCorridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    totalGanadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    fechaUltimaCorrida = Column(Date, nullable=False, server_default=text("'1952-11-19'"))
    refUltCorrida = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    categoria = Column(VARCHAR(2), nullable=False, server_default=text("'D'"))
    descargo = Column(TINYINT, nullable=False, server_default=text("'0'"))
    estadisticaAnual = Column(TINYINT, nullable=False, server_default=text("'0'"))
    corrCesped = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganCesped = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(11, 2), nullable=False, server_default=text("'0.00'"))

    reuniones_caballos = relationship("ReunionCaballos", back_populates="jinete")


class Padrillos(Base):
    __tablename__ = 'Padrillos'

    idPadre = Column(MEDIUMINT, primary_key=True)
    padre = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasClasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))

    caballos = relationship("Caballos", back_populates="padrillo")


class Paises(Base):
    __tablename__ = 'Paises'

    idPais = Column(TINYINT, primary_key=True)
    inicialesPais = Column(CHAR(4), nullable=False, server_default=text("''"))
    nombre = Column(CHAR(25), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    quintos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    clasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(10, 0), nullable=False, server_default=text("'0'"))

    # Relación con Caballos (un país puede tener muchos caballos)
    caballos = relationship("Caballos", back_populates="pais")

class Prensa(Base):
    __tablename__ = 'Prensa'

    idMedio = Column(SMALLINT, primary_key=True)
    medioJCP = Column(VARCHAR(100), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    medioStart = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    condensadoMedio = Column(Float, nullable=False, server_default=text("'100'"))
    pronosticador = Column(VARCHAR(50), nullable=False, server_default=text("''"))
    email = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    activo = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    concreto = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    tipo = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    puntajeAnual = Column(Float)
    participaciones = Column(SmallInteger)


class Preparadores(Base):
    __tablename__ = 'Preparadores'

    idPreparador = Column(MEDIUMINT, primary_key=True)
    preparador = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    jcp = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    estudie = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    condensado = Column(Float, nullable=False, server_default=text("'100'"))
    apellido = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    nombre = Column(VARCHAR(20), nullable=False, server_default=text("''"))
    inicialesNombre = Column(VARCHAR(10), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasDistintas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    quintos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    noPremio = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    boletosJugados = Column(Float, nullable=False, server_default=text("'0'"))
    boletosGanados = Column(Float, nullable=False, server_default=text("'0'"))
    favorito = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasFavorito = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    nCaballos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasClasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasClasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    activo = Column(TINYINT, nullable=False, server_default=text("'1'"))
    ordenEstadistica = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sinGanar = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasUltSemana = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasUltSemana = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ultFecha = Column(Date, nullable=False, server_default=text("'1952-11-19'"))
    ultReferencia = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCambioCesped = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCambioCesped = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCambioArena = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCambioArena = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasReap1 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasReap1 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasReap2 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasReap2 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasReap3 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasReap3 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCambioCorta = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCambioCorta = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCambioLarga = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCambioLarga = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCambioPrep = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCambioPrep = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasHandicap = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasHandicap = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasCondicional = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasCondicional = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasDebutantes = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasDebutantes = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridas2doDebut = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas2doDebut = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    estadisticaAnual = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))

    reuniones_caballos = relationship("ReunionCaballos", back_populates="preparador")


class FechasSemana(Base):
    __tablename__ = 'fechasSemana'

    id = Column(INTEGER, primary_key=True)
    inicioSemana = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    finSemana = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    inicioResultados = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    finResultados = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    inicioTemporada = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    finTemporada = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    fechaMartes = Column(Date, server_default=text("'2024-01-01'"))


class Caballos(Base):
    __tablename__ = 'Caballos'

    idCaballo = Column(MEDIUMINT, primary_key=True)
    nombre = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    marcadorStart = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    modalidad = Column(CHAR(1), nullable=False, server_default=text("''"))
    # idPais = Column(TINYINT, nullable=False, server_default=text("'1'"))
    idPais = Column(
        TINYINT,
        ForeignKey('Paises.idPais', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        server_default=text("'1'")
    )
    sexo = Column(CHAR(1), nullable=False, server_default=text("''"))
    fechaNac = Column(Date, nullable=False, server_default=text("'2024-01-01'"))
    # idColor = Column(TINYINT, nullable=False, server_default=text("'14'"))
    idColor = Column(ForeignKey('Colores.idColor', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, server_default=text("'14'"))
    idPadre = Column(ForeignKey('Padrillos.idPadre', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'3689'"))
    idMadre = Column(ForeignKey('Madres.idMadre', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'3932'"))
    idCriador = Column(ForeignKey('Criadores.idCriador', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'3561'"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(TINYINT, nullable=False, server_default=text("'0'"))
    corridasT = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasT = Column(TINYINT, nullable=False, server_default=text("'0'"))
    placesT = Column(TINYINT, nullable=False, server_default=text("'0'"))
    tercerosT = Column(TINYINT, nullable=False, server_default=text("'0'"))
    cuartosT = Column(TINYINT, nullable=False, server_default=text("'0'"))
    clasicosT = Column(TINYINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    sumasGanadasC = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    lasix = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    testosterona = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    corridasC = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasC = Column(TINYINT, nullable=False, server_default=text("'0'"))
    placesC = Column(TINYINT, nullable=False, server_default=text("'0'"))
    tercerosC = Column(TINYINT, nullable=False, server_default=text("'0'"))
    cuartosC = Column(TINYINT, nullable=False, server_default=text("'0'"))
    clasicosC = Column(TINYINT, nullable=False, server_default=text("'0'"))
    extranjero = Column(CHAR(4), nullable=False, server_default=text("''"))
    sinPremio = Column(TINYINT, nullable=False, server_default=text("'0'"))
    sinGanar = Column(TINYINT, nullable=False, server_default=text("'0'"))

    criador = relationship('Criadores', back_populates="caballos")
    madre = relationship("Madres", back_populates="caballos")
    padrillo = relationship('Padrillos', back_populates="caballos")
    aprontes = relationship("Aprontes", back_populates="caballo")
    color = relationship("Colores", back_populates="caballos")
    # Relación con Paises (un caballo pertenece a un solo país)
    pais = relationship("Paises", back_populates="caballos")

class ReunionCarreras(Base):
    __tablename__ = 'ReunionCarreras'
    __table_args__ = (
        Index('idx_reunioncarreras_fecha_referencia', 'fecha', 'referencia', unique=True),
    )

    idHipodromo = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, primary_key=True, nullable=False, index=True)
    referencia = Column(SMALLINT, primary_key=True, nullable=False, index=True)
    distancia = Column(SMALLINT, server_default=text("'0'"))
    pista = Column(CHAR(1))
    noche = Column(SmallInteger, server_default=text("'0'"))
    ordenDeCarrera = Column(TINYINT, server_default=text("'1'"))
    idCondicion = Column(SMALLINT, server_default=text("'1'"))
    idCondicionEstudie = Column(ForeignKey('CondicionesNuevas.idCondicion', ondelete='SET NULL', onupdate='CASCADE'), index=True, server_default=text("'1'"))
    tiempo = Column(SMALLINT, server_default=text("'0'"))
    tiempoCentesimos = Column(SMALLINT, server_default=text("'0'"))
    tipoTiempo = Column(TINYINT, server_default=text("'0'"))
    baranda = Column(TINYINT, server_default=text("'0'"))
    record = Column(TINYINT, server_default=text("'0'"))
    idClasico = Column(SMALLINT, index=True)  # Sin ForeignKey
    idPremio = Column(SMALLINT, index=True)
    corrieron = Column(TINYINT, server_default=text("'0'"))
    premio1 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio2 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio3 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio4 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio5 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio6 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio7 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premio8 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional1 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional2 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional3 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional4 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional5 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional6 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional7 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioAdicional8 = Column(DECIMAL(9, 2), server_default=text("'0.00'"))
    premioExtra = Column(DECIMAL(9, 2), server_default=text("(0)"))
    idStarter = Column(TINYINT, server_default=text("'4'"))
    corrida = Column(TINYINT, server_default=text("'0'"))
    diagramacion = Column(TINYINT, server_default=text("'0'"))
    idBono = Column(TINYINT, server_default=text("'0'"))
    distanciamiento = Column(TINYINT, server_default=text("'0'"))
    lote = Column(VARCHAR(3), server_default=text("''"))
    tipo = Column(VARCHAR(3), server_default=text("''"))
    minMax = Column(VARCHAR(6), server_default=text("''"))
    sepGanDist = Column(VARCHAR(10), server_default=text("''"))
    totalBoletos = Column(DECIMAL(7, 2), server_default=text("'0.00'"))

    condicion_nueva = relationship('CondicionesNuevas', back_populates="reunion_carreras")
    clasico = relationship('Clasicos', 
                          back_populates="reunion_carreras",
                          primaryjoin="ReunionCarreras.idClasico == Clasicos.idClasico",
                          foreign_keys="ReunionCarreras.idClasico")
    reuniones_caballos = relationship("ReunionCaballos", back_populates="reunion_carrera")


class Aprontes(Base):
    __tablename__ = 'Aprontes'
    __table_args__ = (
        Index('idx_fecha', 'fecha', 'idCaballo'),
    )

    id = Column(INTEGER, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False)
    idCaballo = Column(ForeignKey('Caballos.idCaballo', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    jinete = Column(VARCHAR(15), nullable=False, server_default=text("''"))
    distancia = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    tiempo = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    disFin1 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    tpoFin1 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    disFin2 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    tpoFin2 = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    pista = Column(VARCHAR(35), nullable=False, server_default=text("'0'"))
    calificacion = Column(VARCHAR(3), nullable=False, server_default=text("''"))

    caballo = relationship('Caballos', back_populates="aprontes")


class Separaciones(Base):
    __tablename__ = 'Separaciones'

    idSeparacion = Column(TINYINT, primary_key=True)
    quintos = Column(TINYINT, server_default=text("'0'"))
    separacion = Column(VARCHAR(17), server_default=text("''"))
    separacionReal = Column(DECIMAL(5, 2), server_default=text("'0.00'"))
    sepEstudie = Column(VARCHAR(17), server_default=text("''"))
    sepEstudieFinal = Column(VARCHAR(17), server_default=text("''"))

    reuniones_caballos = relationship("ReunionCaballos", back_populates="separacion")


class Starters(Base):
    __tablename__ = 'Starters'

    idStarter = Column(TINYINT, primary_key=True)
    starterJCP = Column(VARCHAR(15))
    starterEstudie = Column(VARCHAR(30))


class Studs(Base):
    __tablename__ = 'Studs'

    idStud = Column(MEDIUMINT, primary_key=True)
    idHipodromo = Column(TINYINT, nullable=False, server_default=text("'0'"))
    stud = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    minusculas = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    breve = Column(VARCHAR(25), nullable=False, server_default=text("''"))
    colores = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    corridas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadas = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    places = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    terceros = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    cuartos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    clasicos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    corridasUSem = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    ganadasUSem = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    carrerasSinGanar = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    activoEstadistica = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    ordenEstadistica = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    sumasGanadas = Column(Float, nullable=False, server_default=text("'0'"))

    reuniones_caballos = relationship("ReunionCaballos", back_populates="stud")


class ReunionCaballos(Base):
    __tablename__ = 'ReunionCaballos'
    __table_args__ = (
        ForeignKeyConstraint(['fecha', 'referencia'], ['ReunionCarreras.fecha', 'ReunionCarreras.referencia'], ondelete='CASCADE', onupdate='CASCADE'),
        Index('idx_reunioncaballos_fecha_referencia', 'fecha', 'referencia')
    )

    idHipodromo = Column(TINYINT, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, primary_key=True, nullable=False, index=True)
    referencia = Column(SMALLINT, primary_key=True, nullable=False, index=True)
    idCaballo = Column(ForeignKey('Caballos.idCaballo'), primary_key=True, nullable=False, index=True)
    kilos = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    k1 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    m1 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    k2 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    m2 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    quintos = Column(TINYINT, nullable=False, server_default=text("'0'"))
    idJinete = Column(ForeignKey('Jinetes.idJinete'), nullable=False, index=True, server_default=text("'0'"))
    idPreparador = Column(ForeignKey('Preparadores.idPreparador'), nullable=False, index=True, server_default=text("'0'"))
    idStud = Column(ForeignKey('Studs.idStud'), nullable=False, index=True, server_default=text("'0'"))
    cajon = Column(VARCHAR(4), nullable=False, server_default=text("''"))
    realCajon = Column(TINYINT, nullable=False, server_default=text("'0'"))
    pareja = Column(TINYINT, nullable=False, server_default=text("'0'"))
    descartado = Column(TINYINT, nullable=False, server_default=text("'0'"))
    puesto = Column(TINYINT, nullable=False, server_default=text("'0'"))
    puestoEstadistico = Column(TINYINT, nullable=False, server_default=text("'0'"))
    idSeparacion = Column(ForeignKey('Separaciones.idSeparacion'), nullable=False, index=True, server_default=text("'1'"))
    votos = Column(TINYINT, nullable=False, server_default=text("'0'"))
    favCatedra = Column(TINYINT, nullable=False, server_default=text("'0'"))
    morningLine1 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    morningLine2 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    boletosGanador = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    boletosPlace = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    boletosReales = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    favorito = Column(TINYINT, nullable=False, server_default=text("'0'"))
    handicap = Column(VARCHAR(4), nullable=False, server_default=text("''"))
    pesoFisico = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    desarrollo = Column(VARCHAR(6), nullable=False, server_default=text("''"))
    corrio = Column(TINYINT, nullable=False, server_default=text("'0'"))
    retirado = Column(TINYINT, nullable=False, server_default=text("'0'"))
    debutante = Column(TINYINT, nullable=False, server_default=text("'0'"))
    reaparicion = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cambioPasto = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cambioArena = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cambioCorta = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cambioLarga = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    cambioPreparador = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    segundoDebut = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    lasix = Column(SET('T', 'L', 'B', 'N'), nullable=False, server_default=text("'N'"))
    dividendoSoles = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    antiFavorito = Column(TINYINT, nullable=False, server_default=text("'0'"))
    diagramacion = Column(TINYINT, nullable=False, server_default=text("'0'"))
    empate = Column(TINYINT, nullable=False, server_default=text("'0'"))
    premioGanado = Column(DECIMAL(9, 2), nullable=False, server_default=text("'0.00'"))
    sinGanar = Column(SmallInteger, nullable=False, server_default=text("'9999'"))

    reunion_carrera = relationship("ReunionCarreras", back_populates="reuniones_caballos")
    jinete = relationship("Jinetes", back_populates="reuniones_caballos")
    preparador = relationship("Preparadores", back_populates="reuniones_caballos")
    stud = relationship("Studs", back_populates="reuniones_caballos")
    separacion = relationship("Separaciones", back_populates="reuniones_caballos")

    # comentarios = relationship("Comentarios", back_populates="reunion_caballo")
    caballo = relationship("Caballos")
    contratiempos = relationship("Contratiempos", secondary="ReunionContratiempos", back_populates="reuniones_caballos")
    comentarios = relationship("Comentarios", back_populates="reunion_caballo")

class ReunionContratiempos(Base):
    __tablename__ = 'ReunionContratiempos'
    __table_args__ = (
        ForeignKeyConstraint(['fecha', 'referencia', 'idCaballo'], ['ReunionCaballos.fecha', 'ReunionCaballos.referencia', 'ReunionCaballos.idCaballo'], ondelete='CASCADE', onupdate='CASCADE'),
        Index('fk_reunioncontratiempos_reunioncaballos', 'fecha', 'referencia', 'idCaballo')
    )

    fecha = Column(Date, primary_key=True, nullable=False)
    referencia = Column(SMALLINT, primary_key=True, nullable=False)
    idCaballo = Column(MEDIUMINT, primary_key=True, nullable=False)
    idContratiempo = Column(ForeignKey('Contratiempos.idContratiempo'), nullable=False, index=True)
    orden = Column(TINYINT, primary_key=True, nullable=False)


class ReunionApuestas(Base):
    __tablename__ = 'ReunionApuestas'
    __table_args__ = (
        ForeignKeyConstraint(['idHipodromo', 'fecha', 'referencia'],
                             ['ReunionCarreras.idHipodromo','ReunionCarreras.fecha','ReunionCarreras.referencia'],
                             ondelete='CASCADE', onupdate='CASCADE'),
        Index('ReuApuIndex', 'idHipodromo', 'fecha', 'referencia', 'idApuesta')
    )

    idHipodromo = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, primary_key=True, nullable=False)
    referencia = Column(SMALLINT, primary_key=True, nullable=False)
    idApuesta = Column(TINYINT, nullable=False, server_default=text("'0'"))
    quedoPozo1 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    dividendo1 = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"))
    quedoPozo2 = Column(TINYINT, nullable=False, server_default=text("'0'"))
    dividendo2 = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"))
    jugado = Column(DECIMAL(8, 2), nullable=False, server_default=text("'0.00'"))

    reunion_carrera = relationship("ReunionCarreras", backref="reunion_apuestas")


class ReunionPozos(Base):
    __tablename__ = 'ReunionPozos'
    __table_args__ = (
        ForeignKeyConstraint(['idHipodromo', 'fecha', 'referencia'],
                             ['ReunionCarreras.idHipodromo','ReunionCarreras.fecha','ReunionCarreras.referencia'],
                             ondelete='CASCADE', onupdate='CASCADE'),
    )

    idHipodromo = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    fecha = Column(Date, primary_key=True, nullable=False)
    referencia = Column(SMALLINT, primary_key=True, nullable=False)
    idApuesta = Column(TINYINT, nullable=False)
    acumulado = Column(DECIMAL(8, 2))
    tipoPozo = Column(TINYINT)
    pozoProGar = Column(DECIMAL(8, 2))

    reunion_carrera = relationship("ReunionCarreras", backref="reunion_pozos")
import catalogoData from '@/data/catalogoTipologias.json';

/**
 * Mapeo de subsistema a clave de tipología
 */
export const SUBSISTEMA_A_TIPOLOGIA = {
  'SPT - SISTEMA PUESTA A TIERRA': 'TIPOLOGIA_1',
  'PE - GRUPO ELECTROGENO': 'TIPOLOGIA_2',
  'AA - AIRES ACONDICIONADOS': 'TIPOLOGIA_3',
  'PW - POWER': 'TIPOLOGIA_4',
  'MT-BT - MEDIA Y BAJA TENSION': 'TIPOLOGIA_5'
};

/**
 * Obtener la clave de tipología a partir del string del subsistema
 */
export function getTipologiaKeyFromSubsistema(subsistema) {
  if (!subsistema) return 'TIPOLOGIA_1';
  const str = String(subsistema).trim().toUpperCase();
  
  if (SUBSISTEMA_A_TIPOLOGIA[str]) {
    return SUBSISTEMA_A_TIPOLOGIA[str];
  }
  
  if (str.includes('SPT') || str.includes('TIERRA') || str.includes('PUESTA')) {
    return 'TIPOLOGIA_1';
  }
  if (str.includes('PE') || str.includes('ELECTROGEN') || str.includes('PLANTA')) {
    return 'TIPOLOGIA_2';
  }
  if (str.includes('AA') || str.includes('AIRE') || str.includes('CLIMA')) {
    return 'TIPOLOGIA_3';
  }
  if (str.includes('PW') || str.includes('POWER') || str.includes('FUERZA') || str.includes('RECTIF')) {
    return 'TIPOLOGIA_4';
  }
  if (str.includes('MT') || str.includes('BT') || str.includes('TENSION') || str.includes('TENSIÓN')) {
    return 'TIPOLOGIA_5';
  }
  
  return 'TIPOLOGIA_1';
}

/**
 * Obtener los datos completos de una tipología
 */
export function getTipologiaData(tipologiaKey) {
  return catalogoData[tipologiaKey] || catalogoData['TIPOLOGIA_1'];
}

/**
 * Obtener todas las tipologías
 */
export function getAllTipologias() {
  return catalogoData;
}

export default catalogoData;

import client from './client';

export const getOts = async () => {
  const response = await client.get('/ots');
  return response.data.data;
};

export const getOtDetail = async (otId) => {
  const response = await client.get(`/ots/${otId}`);
  return response.data.data;
};

export const createOt = async (otData) => {
  const response = await client.post('/ots', otData);
  return response.data;
};

export const updateOt = async (otId, otData) => {
  const response = await client.put(`/ots/${otId}`, otData);
  return response.data;
};

export const updateOtEstado = async (otId, { estado, progreso }) => {
  const response = await client.put(`/ots/${otId}/estado`, { estado, progreso });
  return response.data;
};

export const uploadEvidencia = async (otId, evidenciaData) => {
  const response = await client.post(`/ots/${otId}/evidencia`, evidenciaData);
  return response.data;
};

export const deleteEvidencia = async (evidenciaId) => {
  const response = await client.delete(`/evidencias/${evidenciaId}`);
  return response.data;
};

export const syncRepuestos = async (otId, repuestos) => {
  const response = await client.post(`/ots/${otId}/repuestos`, { repuestos });
  return response.data;
};

export const cerrarOt = async (otId, cierreData) => {
  const response = await client.post(`/ots/${otId}/cerrar`, cierreData);
  return response.data;
};

export const getOperadores = async () => {
  const response = await client.get('/operadores');
  return response.data.data;
};

export default {
  getOts,
  getOtDetail,
  createOt,
  updateOt,
  updateOtEstado,
  uploadEvidencia,
  deleteEvidencia,
  syncRepuestos,
  cerrarOt,
  getOperadores
};

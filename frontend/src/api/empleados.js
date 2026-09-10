import client from './client';

export const getEmpleados = async () => {
  const response = await client.get('/empleados');
  return response.data.data;
};

export const createEmpleado = async (empleadoData) => {
  const response = await client.post('/empleados', empleadoData);
  return response.data;
};

export const updateEmpleado = async (id, empleadoData) => {
  const response = await client.put(`/empleados/${id}`, empleadoData);
  return response.data;
};

export const getCuadrillas = async () => {
  const response = await client.get('/cuadrillas');
  return response.data.data;
};

export const createCuadrilla = async (cuadrillaData) => {
  const response = await client.post('/cuadrillas', cuadrillaData);
  return response.data;
};

export default {
  getEmpleados,
  createEmpleado,
  updateEmpleado,
  getCuadrillas,
  createCuadrilla
};

import client from './client';

export const getSitios = async (params = {}) => {
  const response = await client.get('/sitios', { params });
  return response.data;
};

export const getSitio = async (id) => {
  const response = await client.get(`/sitios/${id}`);
  return response.data;
};

export const getSitiosStats = async () => {
  const response = await client.get('/sitios/stats/resumen');
  return response.data;
};

export const getSitiosFiltros = async () => {
  const response = await client.get('/sitios/filtros');
  return response.data;
};

export const selectSitios = async (search = '', limit = 30) => {
  const response = await client.get('/sitios/select', {
    params: { search, limit }
  });
  return response.data;
};

export const createSitio = async (data) => {
  const response = await client.post('/sitios', data);
  return response.data;
};

export const updateSitio = async (id, data) => {
  const response = await client.put(`/sitios/${id}`, data);
  return response.data;
};

import client from './client';

export const authApi = {
  login(credentials) {
    return client.post('/login', credentials);
  },
  getUserProfile() {
    return client.get('/user');
  }
};

export default authApi;

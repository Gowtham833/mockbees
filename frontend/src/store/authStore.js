import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/authService';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const response = await authService.login(email, password);
          const { access_token, user } = response.data;
          localStorage.setItem('mockbees_token', access_token);
          
          set({ 
            token: access_token, 
            user: user || { email, name: email.split('@')[0] }, 
            isAuthenticated: true, 
            isLoading: false 
          });
          return true;
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (name, email, password) => {
        set({ isLoading: true });
        try {
          const registerResponse = await authService.register(name, email, password);
          const { access_token, user } = registerResponse.data;
          localStorage.setItem('mockbees_token', access_token);
          
          set({ 
            token: access_token, 
            user: user || { email, name },
            isAuthenticated: true, 
            isLoading: false 
          });
          return true;
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem('mockbees_token');
        set({ user: null, token: null, isAuthenticated: false });
      },

      loadUser: async () => {
        const token = localStorage.getItem('mockbees_token');
        if (!token) return;
        
        set({ isLoading: true });
        try {
          const response = await authService.getProfile();
          set({ 
            user: response.data,
            token,
            isAuthenticated: true,
            isLoading: false
          });
        } catch (error) {
          localStorage.removeItem('mockbees_token');
          set({ user: null, token: null, isAuthenticated: false, isLoading: false });
        }
      },
      
      setUser: (user) => set({ user }),
    }),
    {
      name: 'mockbees-auth',
      partialize: (state) => ({ token: state.token, user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);

export default useAuthStore;

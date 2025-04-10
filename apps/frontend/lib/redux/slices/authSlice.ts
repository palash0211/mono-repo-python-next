import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit"
import { api } from "@/lib/api"
import Cookies from "js-cookie"

interface AuthState {
  token: string | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  token: null,
  isAuthenticated: false,
  loading: false,
  error: null,
}

export const login = createAsyncThunk(
  "auth/login",
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await api.post("/api/auth/login", {
        username: email, // FastAPI OAuth2 expects 'username'
        password,
      })

      const { access_token } = response.data

      // Store token in cookie
      Cookies.set("token", access_token, { expires: 1 }) // 1 day

      return access_token
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || "Login failed")
    }
  },
)

export const logout = createAsyncThunk("auth/logout", async (_, { dispatch }) => {
  // Remove token from cookie
  Cookies.remove("token")
  return null
})

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload
      state.isAuthenticated = true
    },
    clearAuth: (state) => {
      state.token = null
      state.isAuthenticated = false
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.token = action.payload
        state.isAuthenticated = true
        state.loading = false
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
      .addCase(logout.fulfilled, (state) => {
        state.token = null
        state.isAuthenticated = false
      })
  },
})

export const { setToken, clearAuth } = authSlice.actions

export default authSlice.reducer


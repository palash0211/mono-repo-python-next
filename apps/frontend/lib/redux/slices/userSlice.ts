import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit"
import { api } from "@/lib/api"

interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  is_superuser: boolean
}

interface UserState {
  data: User | null
  loading: boolean
  error: string | null
}

const initialState: UserState = {
  data: null,
  loading: false,
  error: null,
}

export const fetchCurrentUser = createAsyncThunk("user/fetchCurrentUser", async (_, { rejectWithValue }) => {
  try {
    const response = await api.get("/api/users/me")
    return response.data
  } catch (error: any) {
    return rejectWithValue(error.response?.data?.detail || "Failed to fetch user")
  }
})

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.data = action.payload
    },
    clearUser: (state) => {
      state.data = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCurrentUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.data = action.payload
        state.loading = false
      })
      .addCase(fetchCurrentUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
  },
})

export const { setUser, clearUser } = userSlice.actions

export default userSlice.reducer


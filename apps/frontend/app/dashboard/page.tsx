"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useAppSelector, useAppDispatch } from "@/lib/redux/hooks"
import { fetchCurrentUser } from "@/lib/redux/slices/userSlice"
import { logout } from "@/lib/redux/slices/authSlice"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Dashboard() {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const { data: user, loading } = useAppSelector((state) => state.user)
  const [items, setItems] = useState([])
  const [itemsLoading, setItemsLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login")
    } else {
      dispatch(fetchCurrentUser())
      fetchItems()
    }
  }, [isAuthenticated, dispatch, router])

  const fetchItems = async () => {
    try {
      setItemsLoading(true)
      const response = await api.get("/api/items")
      setItems(response.data)
    } catch (error) {
      console.error("Error fetching items:", error)
    } finally {
      setItemsLoading(false)
    }
  }

  const handleLogout = () => {
    dispatch(logout())
    router.push("/login")
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="mx-auto max-w-7xl">
        <div className="flex items-center justify-between py-4">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <Button onClick={handleLogout} variant="outline">
            Logout
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Welcome, {user?.full_name || "User"}</CardTitle>
              <CardDescription>{user?.email}</CardDescription>
            </CardHeader>
            <CardContent>
              <p>User role: {user?.is_superuser ? "Admin" : "Regular User"}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Items</CardTitle>
              <CardDescription>Your items from the API</CardDescription>
            </CardHeader>
            <CardContent>
              {itemsLoading ? (
                <p>Loading items...</p>
              ) : items.length > 0 ? (
                <ul className="space-y-2">
                  {items.map((item) => (
                    <li key={item.id} className="rounded border p-2">
                      <strong>{item.name}</strong>
                      <p className="text-sm text-gray-500">{item.description}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No items found</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}


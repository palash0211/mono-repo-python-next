"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAppSelector } from "@/lib/redux/hooks"

export default function Home() {
  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login")
    } else {
      router.push("/dashboard")
    }
  }, [isAuthenticated, router])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Loading...</h1>
        <p className="mt-4">Redirecting to the appropriate page</p>
      </div>
    </main>
  )
}


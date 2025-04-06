import Link from 'next/link'
import React from 'react'

const NavBar: React.FC = () => {
  return (
    <nav className="flex justify-between items-center bg-black text-white p-4 px-16">
      <div className="font-bold text-xl">Bilbo Baggins</div>
      <div>
        <Link href="/signin" className="mr-4 hover:text-gray-300">
          Sign In
        </Link>
        <Link href="/signup" className="hover:text-gray-300">
          Sign Up
        </Link>
      </div>
    </nav>
  )
}

export default NavBar

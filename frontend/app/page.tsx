import React from 'react'

const HomePage: React.FC = () => {
  return (
    <section className="flex flex-col items-center justify-center h-[calc(100vh-4rem)]">
      <h1 className="text-4xl font-bold mb-4">Welcome to Bilbo Baggins</h1>
      <p className="text-xl mb-8">Your AI companion awaits!</p>
      <button className="bg-black text-white py-2 px-4 rounded">
        Get Started
      </button>
    </section>
  )
}

export default HomePage

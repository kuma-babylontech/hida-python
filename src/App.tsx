import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import { Home } from './pages/Home'
import { SlideViewer } from './pages/SlideViewer'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
      </Route>
      <Route path="/slides/:id" element={<SlideViewer />} />
    </Routes>
  )
}

export default App

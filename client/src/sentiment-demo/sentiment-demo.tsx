import { useState } from "react"

function Sentiment_demo() {
    const [sentiment, setSentiment] = useState('neutral')
    return (
        <div>
            {/* buttons to simulate sentiments */}
            <button onClick={()=>{setSentiment('happy')}}>Simulate happy</button>
            <button onClick={()=>{setSentiment('neutral')}}>Simulate neutral</button>
            <button onClick={()=>{setSentiment('sad/concerned')}}>Simulate sad/concerned</button>
            
            {sentiment=='happy' && <img src='https://i.pinimg.com/736x/a8/d8/cd/a8d8cd1903ed8d0b8aa20f398772210f.jpg'/>}
            {sentiment=='neutral' && <img src='https://familyguyaddicts.com/wp-content/uploads/2014/04/peter-animation-033idlepic4x.png'/>}
            {sentiment=='sad/concerned' && <img src='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3a21ce2c-aa51-4d33-bca0-e83994620ee0/dg8igc3-01f1ddc2-0e80-4070-9a0d-87fa4ed7d6df.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzNhMjFjZTJjLWFhNTEtNGQzMy1iY2EwLWU4Mzk5NDYyMGVlMFwvZGc4aWdjMy0wMWYxZGRjMi0wZTgwLTQwNzAtOWEwZC04N2ZhNGVkN2Q2ZGYuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.sPd2B2LZeVH7Pa0A9jFGeB6u18SGINIWQYGa95_0hNc'/>}
        </div> 
        
    )
}

export default Sentiment_demo
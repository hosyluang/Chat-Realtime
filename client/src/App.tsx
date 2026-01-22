// client/src/App.tsx
import { useState } from 'react';
import api from './api';

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            // --- SỬA ĐOẠN NÀY ---
            // Tạo Form Data chuẩn x-www-form-urlencoded
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            // Gửi đi (Không gửi object JSON {} nữa mà gửi formData)
            const response = await api.post('/auth/signin', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            // --------------------

            setToken(response.data.access_token);
            alert('Đăng nhập thành công!');
        } catch (err: any) {
            console.error(err);
            setError('Sai tài khoản hoặc mật khẩu!');
        }
    };

    return (
        <div style={{ padding: '50px', maxWidth: '400px', margin: '0 auto' }}>
            <h2>Test Login System</h2>

            {!token ? (
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <input
                        placeholder='Username'
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{ padding: '10px' }}
                    />
                    <input
                        type='password'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ padding: '10px' }}
                    />
                    <button type='submit' style={{ padding: '10px', background: 'blue', color: 'white' }}>
                        Đăng nhập
                    </button>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                </form>
            ) : (
                <div>
                    <h3 style={{ color: 'green' }}>Login Success!</h3>
                    <p>Token của bạn:</p>
                    <textarea readOnly value={token} style={{ width: '100%', height: '100px' }} />
                    <button onClick={() => setToken('')}>Đăng xuất</button>
                </div>
            )}
        </div>
    );
}

export default App;

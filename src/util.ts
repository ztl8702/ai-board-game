export function isProduction(): boolean {
    if (getEnv("WYB_ENVIRONMENT") == 'production') return true;
    return false;
}

export function getEnv(key: string) {
    return process.env[key];
}

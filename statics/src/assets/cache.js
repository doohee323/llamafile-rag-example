export function getCacheKey(group, cacheKey) {
    cacheKey = cacheKey.replace(/&/g, '').replace(/\?/g, '').replace(/,/g, '');
    return group + '-' + cacheKey;
}

export function setCache(group, cacheKey, cacheData, expires) {
    let newCacheKey = getCacheKey(group, cacheKey);
    if (expires === undefined || expires === null) {
        expires = 10000;
    }
    let date = new Date();
    let schedule = Math.round((date.setSeconds(date.getSeconds() + expires)) / 1000);
    try {
        sessionStorage.setItem(newCacheKey, cacheData);
        sessionStorage.setItem(newCacheKey + '_time', schedule);
    } catch (e) {
        initSCacheEx(group, cacheKey);
        sessionStorage.setItem(newCacheKey, cacheData);
        sessionStorage.setItem(newCacheKey + '_time', schedule);
    }
}

export function getCache(group, cacheKey) {
    try {
        let newCacheKey = getCacheKey(group, cacheKey);
        let date = new Date();
        let current = Math.round(date / 1000);
        let stored_time = sessionStorage.getItem(newCacheKey + '_time');
        if (stored_time === undefined || stored_time === null) {
            stored_time = 0;
        }
        if (stored_time < current) {
            initSCacheEx(group, cacheKey);
            return '';
        } else {
            const val = sessionStorage.getItem(newCacheKey);
            if (!val || val === 'null' || val === 'undefined') {
                sessionStorage.setItem(newCacheKey, '');
                return '';
            }
            return sessionStorage.getItem(newCacheKey);
        }
    } catch (e) {
        console.log(e);
    }
}

export function initSCacheEx(group, cacheKey) {
    cacheKey = getCacheKey(group, cacheKey);
    sessionStorage.setItem(cacheKey, null);
    sessionStorage.setItem(cacheKey + '_time', null);
}

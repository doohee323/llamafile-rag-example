import HomePage from "@/components/Home-page.vue";
import NotfoundPage from "@/components/Notfound-page.vue";
import Upload from "@/components/Upload-page.vue";

export default [
    {
        path: '/',
        component: HomePage,
        name: 'Home',
    },
    {
        path: '/upload',
        component: Upload,
        name: 'Upload Image',
    },
    {
        path: '*', beforeEnter: (to, from, next) => {
            next('/')
        }
    },
    {
        path: '/404',
        name: 'Not Found',
        component: NotfoundPage
    },
]
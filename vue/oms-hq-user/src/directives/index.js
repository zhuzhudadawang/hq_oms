import permission from './permission'
import role from './role'

export default {
  install(app) {
    app.directive('permission', permission)
    app.directive('role', role)
  }
}

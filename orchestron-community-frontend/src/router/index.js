import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Layout from '../views/layout/Layout'
import Login from '../views/login/index'
import Forbidden from '@/components/Errors/Forbidden'
import NotFound from '@/components/Errors/NotFound'
import Error from '@/components/Errors/Error'
import dashboard from '../views/dashboard/index'
import ChangePassword from '../views/User/ChangePassword'
import UserProfile from '../views/User/UserProfile'
import OpenVulnerabilities from '../views/OpenVulnerabilities/Index'
import ClosedVulnerabilities from '../views/ClosedVulnerabilities/index'
import ToolIndex from '../views/Tool/index'
import SeverityWise from '../views/SeverityWiseView/index'
import IndividualVulnerability from '../views/IndividualVulnerability/index'
import ClosedIndividualVul from '../views/IndividualVulnerability/ClosedIndividualVul'
import IndividualReqResp from '../views/IndividualVulnerability/IndividualReqResp'
import Projects from '../views/Projects/index'
import IndividualProject from '../views/Projects/IndividualProject'
import IndividualApplication from '../views/Applications/index'
import AppOpenVulnerabilities from '../views/Applications/OpenVulnerabilities'
import AppClosedVulnerabilities from '../views/Applications/ClosedVulnerabilities'
import AppSeverityWise from '../views/Applications/SeverityWise'
import IndividualScan from '../views/Scans/Index'
import ScansIndividualVulInfo from '../views/Scans/ScansIndividualVulInfo'
import ScanSeverityWise from '../views/Scans/SeverityWise'
import WebHook from '../views/Webhooks/index'
import Engagements from '../views/Engagements/index'
import individualEngagement from '../views/Engagements/individualEngagement'
import EngagementSeverityWise from '../views/Engagements/SeverityWise'
import Settings from '../views/Settings/index'
import IndividualOrg from '../views/Settings/IndividualOrg'

export const constantRouterMap = [
  { path: '/', component: Login, hidden: true },
  { path: '/login', component: Login, hidden: true },
  { path: '/forbidden', component: Forbidden },
  { path: '/not_found', component: NotFound },
  { path: '/error', component: Error },
  {
    path: '/org',
    component: Layout,
    meta: { title: 'Dashboard', icon: 'Dashboard' },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: dashboard,
        meta: { title: 'Dashboard', icon: 'Dashboard' }
      },
      {
        path: 'openvuls',
        component: OpenVulnerabilities,
        name: 'OpenVulnerabilities',
        meta: {
          title: 'Open Vulnerabilities',
          icon: 'Open Vulnerabilities'
        }
      },
      {
        path: 'closed_vul',
        component: ClosedVulnerabilities,
        name: 'ClosedVulnerabilities',
        meta: {
          title: 'Closed Vulnerabilities',
          icon: 'Closed Vulnerabilities'
        }
      },
      {
        path: 'severity_wise/:sev',
        component: SeverityWise,
        name: 'Severity-Wise',
        meta: {
          title: 'Severity Wise',
          icon: 'Severity Wise'
        }
      },
      {
        path: 'individual_vul/:appName/:vulName/:cwe',
        component: IndividualVulnerability,
        name: 'IndividualVulnerability',
        meta: {
          title: 'Individual Vulnerability',
          icon: 'Individual Vulnerability'
        }
      },
      {
        path: 'individual/closed_vul/:appName/:vulName/:cwe',
        component: ClosedIndividualVul,
        name: 'Closed IndividualVulnerability',
        meta: {
          title: 'Closed Individual Vulnerability',
          icon: 'Closed Individual Vulnerability'
        }
      },
      {
        path: 'individual_vul_req_resp/:appName/:vulName/:cwe/:url',
        component: IndividualReqResp,
        name: 'IndividualVulnerability Request and Response',
        meta: {
          title: 'IndividualVulnerability Request and Response',
          icon: 'IndividualVulnerability Request and Response'
        }
      },
      {
        path: 'individual_tool/:tool',
        component: ToolIndex,
        name: 'Individual Tool',
        meta: {
          title: 'Individual Tool',
          icon: 'Individual Tool'
        }
      },
      {
        path: 'change_password',
        component: ChangePassword,
        name: 'Change Password',
        meta: {
          title: 'Change Password',
          icon: 'Change Password'
        }
      },
      {
        path: 'profile',
        component: UserProfile,
        name: 'Profile',
        meta: {
          title: 'Profile',
          icon: 'Profile'
        }
      }
    ]
  },
  {
    path: '/projects',
    component: Layout,
    meta: {
      title: 'Projects',
      icon: 'project'
    },
    children: [
      {
        path: '',
        name: 'Projects',
        component: Projects,
        meta: { title: 'Projects', icon: 'project' }
      },
      {
        path: 'individual_project/:projectId',
        name: 'Individual Project',
        component: IndividualProject,
        meta: { title: 'Individual Project' }
      },
      {
        path: 'individual_application/:applicationId',
        name: 'Individual Application',
        component: IndividualApplication,
        meta: { title: 'Individual Application' }
      },
      {
        path: 'individual_application/open_vul/:applicationId',
        name: 'Individual Application Open Vulnerabilities',
        component: AppOpenVulnerabilities,
        meta: { title: 'Individual Application Open Vulnerabilities' }
      },
      {
        path: 'individual_application/closed_vul/:applicationId',
        name: 'Individual Application Closed Vulnerabilities',
        component: AppClosedVulnerabilities,
        meta: { title: 'Individual Application Closed Vulnerabilities' }
      },
      {
        path: 'individual_application/:applicationId/severity_wise/:sev',
        name: 'individual_application_severity',
        component: AppSeverityWise,
        meta: { title: 'Applications Severity' }
      },
      {
        path: 'individual_application/:applicationId/individual_scan/:scanId',
        name: 'Individual Application Scan',
        component: IndividualScan,
        meta: { title: 'Individual Application Scan' }
      },
      {
        path: 'individual_application/:applicationId/individual_scan/:scanId/individual_vul/:vulId',
        name: 'Scan Wise Vulnerability Info',
        component: ScansIndividualVulInfo,
        meta: { title: 'Scan Wise Vulnerability Info' }
      },
      {
        path: 'individual_application/:applicationId/individual_scan/:scanId/severity_wise/:sev',
        name: 'Scan Wise Severity',
        component: ScanSeverityWise,
        meta: { title: 'Scan Wise Severity' }
      }
    ]
  },
  {
    path: '/webhooks',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Webhook',
        component: WebHook,
        meta: { title: 'Webhooks', icon: 'webhook' }
      }
    ]
  },
  {
    path: '/engagements',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Engagements',
        component: Engagements,
        meta: { title: 'Engagements', icon: 'Engagements' }
      },
      {
        path: 'individual_engagement/:engagementId',
        name: 'Individual Engagement',
        component: individualEngagement,
        meta: { title: 'Individual Engagement', icon: 'Engagements' }
      },
      {
        path: 'individual_engagement/:engagementId/severity_wise/:sev',
        name: 'Severity Wise Engagement',
        component: EngagementSeverityWise,
        meta: { title: 'Severity Wise Engagement', icon: 'Engagements' }
      }
    ]
  },
  {
    path: '/settings',
    component: Layout,
    meta: { title: 'Settings', icon: 'settings' },
    children: [
      {
        path: '',
        name: 'Settings',
        component: Settings,
        meta: { title: 'Settings', icon: 'settings' }
      },
      {
        path: '/settings/individual_org/:orgId',
        component: IndividualOrg,
        name: 'Individual Organization',
        meta: {
          title: 'Individual Organization',
          icon: 'settings'
        }
      }
    ]
  }
]
export default new Router({
  scrollBehavior: () => ({ y: 0 }),
  mode: 'history',
  routes: constantRouterMap
})

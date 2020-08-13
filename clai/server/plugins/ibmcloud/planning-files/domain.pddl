(define (domain kube)
(:requirements :typing :action-costs)

(:types 
object
ptype)

(:predicates
(known ?o - object)
(protocol_type ?p - ptype)
(docker_built)
(docker_running)
(docker_tagged)
(docker_pushed)
(ibmcloud_logged_in)
(ibmcloud_cr_logged_in)
(space_available)
(checked_account)
(is_free_account)
(images_listed)
(deployed)
)

(:functions (total-cost))

(:action set-state
:parameters ()
:precondition 
(and 
)
:effect 
(and 
(increase (total-cost) 1)
(space_available)
(known username)
(known password)
(known name)
(known tag)
(known host_port)
)
)

(:action docker-build
:parameters ()
:precondition 
(and 
(known name)
(known tag)
)
:effect 
(and 
(increase (total-cost) 1)
(docker_built)
)
)

(:action dockerfile-read
:parameters ()
:precondition 
(and 
(docker_built)
)
:effect 
(and 
(increase (total-cost) 1)
(known local_port)
)
)

(:action docker-run
:parameters ()
:precondition 
(and 
(docker_built)
(known host_port)
(known local_port)
)
:effect 
(and 
(increase (total-cost) 1)
(docker_running)
)
)

(:action ibmcloud-login
:parameters ()
:precondition 
(and 
(known username)
(known password)
)
:effect 
(and 
(increase (total-cost) 1)
(ibmcloud_logged_in)
)
)

(:action ibmcloud-cr-login
:parameters ()
:precondition 
(and 
(ibmcloud_logged_in)
)
:effect 
(and 
(increase (total-cost) 1)
(ibmcloud_cr_logged_in)
)
)

(:action get-namespace
:parameters ()
:precondition 
(and 
(ibmcloud_cr_logged_in)
)
:effect 
(and 
(increase (total-cost) 1)
(known namespace)
)
)

(:action docker-tag-for-ibmcloud
:parameters ()
:precondition 
(and 
(docker_built)
(known namespace)
)
:effect 
(and 
(increase (total-cost) 1)
(docker_tagged)
)
)

(:action docker-push
:parameters ()
:precondition 
(and 
(docker_tagged)
(space_available)
)
:effect 
(and 
(increase (total-cost) 1)
(docker_pushed)
)
)

(:action list-images
:parameters ()
:precondition 
(and 
)
:effect 
(and 
(increase (total-cost) 1)
(images_listed)
)
)

(:action get-image-name-to-delete
:parameters ()
:precondition 
(and 
(images_listed)
)
:effect 
(and 
(increase (total-cost) 1)
(known name-to-delete)
)
)

(:action ibmcloud-delete-image
:parameters ()
:precondition 
(and 
(known name-to-delete)
(not (space_available))
)
:effect 
(and 
(increase (total-cost) 1)
(space_available)
)
)

(:action check-account-free
:parameters ()
:precondition 
(and 
(ibmcloud_logged_in)
(not (checked_account))
)
:effect 
(and 
(increase (total-cost) 0)
(checked_account)
(is_free_account)
)
)

(:action check-account-paid
:parameters ()
:precondition 
(and 
(ibmcloud_logged_in)
(not (checked_account))
)
:effect 
(and 
(increase (total-cost) 10)
(checked_account)
(not (is_free_account))
)
)

(:action set-protocol
:parameters ()
:precondition 
(and 
(checked_account)
(is_free_account)
)
:effect 
(and 
(increase (total-cost) 0)
(known protocol)
)
)

(:action ask-protocol
:parameters ()
:precondition 
(and 
(checked_account)
(not (is_free_account))
)
:effect 
(and 
(increase (total-cost) 10)
(known protocol)
)
)

(:action build-yaml
:parameters ()
:precondition 
(and 
(docker_tagged)
(known local_port)
(known host_port)
(known protocol)
)
:effect 
(and 
(increase (total-cost) 1)
(known yaml)
)
)

(:action get-set-cluster-config
:parameters ()
:precondition 
(and 
(known yaml)
)
:effect 
(and 
(known cluster-config)
)
)

(:action kube-deploy
:parameters ()
:precondition 
(and 
(docker_pushed)
(known cluster-config)
)
:effect 
(and 
(increase (total-cost) 1)
(deployed)
)
)


)

